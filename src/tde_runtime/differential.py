"""Generic differential assessment over immutable canonical evidence."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping
from .models import utc_now
from .schemas import SchemaRegistry

class DifferentialError(ValueError): pass

class AssessmentBaselineRegistry:
 def __init__(self, location: str|Path): self.location=Path(location)
 def create(self,evidence:Mapping[str,Any],identifier:str|None=None)->dict[str,Any]:
  SchemaRegistry.validate_assessment(evidence); assessment=evidence['assessment']; digest=evidence['integrity']['contentDigest']
  baseline_id=identifier or 'baseline.'+sha256(digest.encode()).hexdigest()[:16]
  created=utc_now(); record={'baselineId':baseline_id,'assessmentId':assessment['assessmentId'],'assessmentEvidenceId':digest,'repositoryId':evidence['repository']['id'],'assessmentProfile':{'identifier':assessment['profile'],'version':assessment['profileVersion'],'hash':assessment['profileHash']},'schemaVersion':evidence['schemaVersion'],'runtimeVersion':evidence['runtime']['version'],'timestamp':created,'createdAt':created}
  path=self.location/f'{baseline_id}.json'; self.location.mkdir(parents=True,exist_ok=True)
  if path.exists(): raise DifferentialError(f'baseline already exists and is immutable: {baseline_id}')
  path.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n',encoding='utf-8'); return record
 def load(self,reference:str|Path)->dict[str,Any]:
  path=Path(reference); path=path if path.exists() or path.is_absolute() else self.location/f'{reference}.json'
  try: value=json.loads(path.read_text(encoding='utf-8'))
  except (OSError,json.JSONDecodeError) as error: raise DifferentialError(f'cannot load baseline {reference}: {error}') from error
  if not isinstance(value,dict) or not {'baselineId','assessmentEvidenceId','repositoryId','assessmentProfile','schemaVersion','runtimeVersion'}<=set(value): raise DifferentialError('baseline is malformed')
  return value

class DifferentialEngine:
 def compare(self,current:Mapping[str,Any],baseline:Mapping[str,Any],previous:Mapping[str,Any])->dict[str,Any]:
  SchemaRegistry.validate_assessment(current); SchemaRegistry.validate_assessment(previous)
  compatible=(current['repository']['id']==baseline['repositoryId'] and current['schemaVersion']==baseline['schemaVersion'] and current['runtime']['version']==baseline['runtimeVersion'] and current['assessment']['profile']==baseline['assessmentProfile']['identifier'])
  current_id=current['integrity']['contentDigest']; base_id=baseline['assessmentEvidenceId']
  deltas=[]
  old={x['capabilityId']:x for x in previous.get('capabilityResults',[])}
  for item in current.get('capabilityResults',[]):
   cap=item['capabilityId']; classification='NOT_COMPARABLE' if not compatible else 'NEW' if cap not in old else self._classify(current,previous,cap)
   deltas.append({'capabilityId':cap,'classification':classification})
  overall='NOT_COMPARABLE' if not compatible else self._overall([x['classification'] for x in deltas])
  result={'schema':SchemaRegistry.identity('differential-evidence',current['runtime']['version'],str(current['assessment']['profileVersion'])),'differentialId':'differential.'+sha256(f'{current_id}:{baseline["baselineId"]}'.encode()).hexdigest()[:24],'baselineId':baseline['baselineId'],'baselineAssessmentId':baseline['assessmentId'],'currentAssessmentId':current['assessment']['assessmentId'],'baselineEvidenceId':base_id,'currentEvidenceId':current_id,'capabilityDeltas':deltas,'assessmentDelta':overall,'timestamp':utc_now()}
  SchemaRegistry.validate('differential-evidence',result); return result
 @staticmethod
 def _classify(current,previous,cap):
  key=lambda x:(x.get('metricKey'),x.get('scope'),x.get('targetEntityId'))
  before={key(x):x.get('value') for x in previous.get('measurements',[]) if x.get('capabilityId')==cap and isinstance(x.get('value'),(int,float))}
  after={key(x):x.get('value') for x in current.get('measurements',[]) if x.get('capabilityId')==cap and isinstance(x.get('value'),(int,float))}
  shared=[after[x]-before[x] for x in after if x in before]
  if not shared:return 'UNCHANGED'
  return 'REGRESSED' if sum(shared)>0 else 'IMPROVED' if sum(shared)<0 else 'UNCHANGED'
 @staticmethod
 def _overall(values): return 'REGRESSED' if 'REGRESSED' in values else 'IMPROVED' if 'IMPROVED' in values else 'NEW' if 'NEW' in values else 'UNCHANGED'
