library BreastCancerNeoadjuvant

using FHIR version '4.0.1'

include hl7.fhir.uv.cql.FHIRHelpers version '4.0.1' called FHIRHelpers
include CRLCommon called CRLCommon

valueset "Invasive Breast Carcinoma": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-invasive-breast-carcinoma'
valueset "Receptor Results": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-receptor-results'
valueset "Negative Receptor Result": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-negative-receptor-result'
valueset "Estrogen Receptor Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-estrogen-receptor-test'
valueset "Progesterone Receptor Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-progesterone-receptor-test'
valueset "HER2 Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-her2-test'
valueset "Clinical M Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-m-test'
valueset "Clinical M Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-m-categories'
valueset "Clinical M Qualifying Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-m-qualifying-categories'
valueset "Clinical N Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-n-test'
valueset "Clinical N Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-n-categories'
valueset "Clinical N Qualifying Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-n-qualifying-categories'
valueset "Clinical T Test": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-t-test'
valueset "Clinical T Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-t-categories'
valueset "Clinical T Qualifying Categories": 'https://alphora.github.io/hl7-agentic-knowledge-connectathon/fhir/ValueSet/breast-cancer-neoadjuvant-clinical-t-qualifying-categories'

context Patient

/* REFACTOR:grounded (#320, reviewed 557): reserved v1 publication selection helpers. */
define function "__CRL_PublicationSelection_v1_ValidityState"(raw System.String):
  if raw is null then 'missing'
  else if not Matches(raw, '\\A[0-9]{4}(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01])(T([01][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)([.][0-9]+)?(Z|[+-]((0[0-9]|1[0-3]):[0-5][0-9]|14:00)))?)?)?\\z')
    or Substring(raw, 0, 4) = '0000'
    or ToDateTime(Substring(raw, 0, 10)) is null then 'invalid'
  else if Substring(raw, 17, 2) = '60'
    or Matches(raw, '\\A.*[.][0-9]{3}[0-9]*[1-9][0-9]*(Z|[+-]((0[0-9]|1[0-3]):[0-5][0-9]|14:00))\\z') then 'unsupported'
  else 'supported'

/* Full zoned seconds are exact instants in the shared TS comparator. Normalize only comparison
 * precision to milliseconds; never rewrite the candidate's authored validity or resource. */
define function "__CRL_PublicationSelection_v1_ComparisonValue"(raw System.String):
  if Length(raw) > 10 and Substring(raw, 19, 1) != '.' then
    ToDateTime(Substring(raw, 0, 19) + '.000' + Substring(raw, 19))
  else ToDateTime(raw)

/* Bounds cover every possible instant at the calendar's precision and FHIR's +/-14h zone range.
 * UTC is explicit. At year-domain edges null means unbounded for comparison, never missing validity.
 * FHIR rejects years outside 1..9999: no valid instant can precede the first calendar's earliest
 * bound or reach the final calendar's exclusive upper bound. These null edges therefore agree
 * with the finite TS bounds, which can be represented in JS comparison years 0/10000.
 * These computational bounds are never written to a candidate or exposed as its clinical time. */
define function "__CRL_PublicationSelection_v1_CalendarStart"(raw System.String):
  DateTime(ToInteger(Substring(raw, 0, 4)),
    if Length(raw) >= 7 then ToInteger(Substring(raw, 5, 2)) else 1,
    if Length(raw) = 10 then ToInteger(Substring(raw, 8, 2)) else 1,
    0, 0, 0, 0, 0)

define function "__CRL_PublicationSelection_v1_CalendarLower"(raw System.String):
  if "__CRL_PublicationSelection_v1_CalendarStart"(raw) = DateTime(1, 1, 1, 0, 0, 0, 0, 0) then null as System.DateTime
  else "__CRL_PublicationSelection_v1_CalendarStart"(raw) - 14 hours

define function "__CRL_PublicationSelection_v1_CalendarNextStart"(raw System.String):
  if raw in { '9999', '9999-12', '9999-12-31' } then null as System.DateTime
  else if Length(raw) = 4 then "__CRL_PublicationSelection_v1_CalendarStart"(raw) + 1 year
  else if Length(raw) = 7 then "__CRL_PublicationSelection_v1_CalendarStart"(raw) + 1 month
  else "__CRL_PublicationSelection_v1_CalendarStart"(raw) + 1 day

define function "__CRL_PublicationSelection_v1_CalendarUpper"(raw System.String):
  if "__CRL_PublicationSelection_v1_CalendarNextStart"(raw) is null then null as System.DateTime
  else "__CRL_PublicationSelection_v1_CalendarNextStart"(raw) + 14 hours

define function "__CRL_PublicationSelection_v1_MixedCompare"(calendar System.String, instant System.DateTime):
  if "__CRL_PublicationSelection_v1_CalendarLower"(calendar) is not null and instant < "__CRL_PublicationSelection_v1_CalendarLower"(calendar) then 'after'
  else if "__CRL_PublicationSelection_v1_CalendarUpper"(calendar) is not null and instant >= "__CRL_PublicationSelection_v1_CalendarUpper"(calendar) then 'before'
  else 'indeterminate'

define function "__CRL_PublicationSelection_v1_Compare"(left System.String, right System.String):
  if "__CRL_PublicationSelection_v1_ValidityState"(left) = 'invalid' or "__CRL_PublicationSelection_v1_ValidityState"(right) = 'invalid' then 'invalid'
  else if left is null or right is null then 'indeterminate'
  else if "__CRL_PublicationSelection_v1_ValidityState"(left) = 'unsupported' or "__CRL_PublicationSelection_v1_ValidityState"(right) = 'unsupported' then 'unsupported'
  else if Length(left) <= 10 and Length(right) > 10 then "__CRL_PublicationSelection_v1_MixedCompare"(left, "__CRL_PublicationSelection_v1_ComparisonValue"(right))
  else if Length(right) <= 10 and Length(left) > 10 then
    case "__CRL_PublicationSelection_v1_MixedCompare"(right, "__CRL_PublicationSelection_v1_ComparisonValue"(left))
      when 'before' then 'after'
      when 'after' then 'before'
      else 'indeterminate'
    end
  else if "__CRL_PublicationSelection_v1_ComparisonValue"(left) > "__CRL_PublicationSelection_v1_ComparisonValue"(right) then 'after'
  else if "__CRL_PublicationSelection_v1_ComparisonValue"(left) < "__CRL_PublicationSelection_v1_ComparisonValue"(right) then 'before'
  else if "__CRL_PublicationSelection_v1_ComparisonValue"(left) = "__CRL_PublicationSelection_v1_ComparisonValue"(right) then 'equal'
  else 'indeterminate'

define function "__CRL_PublicationSelection_v1_Result"(state System.String, failureCode System.String, conceptId System.String, selected Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, affected List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>):
  Tuple {
    state: state,
    failureCode: failureCode,
    failureMessage: if failureCode is null then null as System.String
      else failureCode + ' in ' + conceptId + ': ' + Combine((affected C return all C.key), ', ')
        + (if failureCode != 'publication-incomparable-validity' then ''
          else if exists (affected C where exists (affected D
            where "__CRL_PublicationSelection_v1_Compare"(C.validity, D.validity) = 'unsupported' return all D) return all C)
            then ': unsupported comparison of validity; correct or exclude the unsupported input'
          else ': overlapping precision of validity; equal-time preference does not resolve overlap'),
    conceptId: conceptId,
    selected: selected,
    affected: affected
  }

define function "__CRL_PublicationSelection_v1_Fail"(failureCode System.String, conceptId System.String, affected List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>):
  "__CRL_PublicationSelection_v1_Result"('failed', failureCode, conceptId, null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String },
    (affected C return all C sort by key, contributorId, arm, retrievedInputIdentity, validity))

define function "__CRL_PublicationSelection_v1_Choose"(latest List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, conceptId System.String, equalTime System.String):
  if Count(latest) = 1 then "__CRL_PublicationSelection_v1_Result"('selected', null, conceptId, singleton from latest, {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>)
  else if equalTime = 'preferLocal' and Count(latest C where C.arm = 'local' return all C) = 1 then
    "__CRL_PublicationSelection_v1_Result"('selected', null, conceptId, singleton from (latest C where C.arm = 'local' return all C), {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>)
  else "__CRL_PublicationSelection_v1_Fail"('publication-ambiguous-selection', conceptId, latest)

define function "__CRL_PublicationSelection_v1_Latest"(candidates List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, conceptId System.String, equalTime System.String):
  if not exists (candidates C
    where not exists (candidates D where not ("__CRL_PublicationSelection_v1_Compare"(C.validity, D.validity) in { 'after', 'equal' }) return all D)
    return all C) then "__CRL_PublicationSelection_v1_Fail"('publication-incomparable-validity', conceptId, candidates)
  else "__CRL_PublicationSelection_v1_Choose"(
    (candidates C where not exists (candidates D where not ("__CRL_PublicationSelection_v1_Compare"(C.validity, D.validity) in { 'after', 'equal' }) return all D) return all C),
    conceptId, equalTime)

define function "__CRL_PublicationSelection_v1_Select"(candidates List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, conceptId System.String, equalTime System.String):
  if exists (candidates C where C.validity is not null and "__CRL_PublicationSelection_v1_ValidityState"(C.validity) = 'invalid' return all C) then
    "__CRL_PublicationSelection_v1_Fail"('publication-invalid-validity', conceptId,
      (candidates C where C.validity is not null and "__CRL_PublicationSelection_v1_ValidityState"(C.validity) = 'invalid' return all C))
  else if exists (candidates C where C.arm != 'inferred' and (C.retrievedInputIdentity is null or C.retrievedInputIdentity = '') return all C) then
    "__CRL_PublicationSelection_v1_Fail"('publication-missing-input-identity', conceptId,
      (candidates C where C.arm != 'inferred' and (C.retrievedInputIdentity is null or C.retrievedInputIdentity = '') return all C))
  else if exists (candidates C where
    Count(candidates D where D.key = C.key return all D) > 1
    or (C.retrievedInputIdentity is not null and Count(candidates D where D.contributorId = C.contributorId and D.retrievedInputIdentity = C.retrievedInputIdentity return all D) > 1)
    return all C) then
    "__CRL_PublicationSelection_v1_Fail"('publication-duplicate-input', conceptId,
      (candidates C where Count(candidates D where D.key = C.key return all D) > 1
        or (C.retrievedInputIdentity is not null and Count(candidates D where D.contributorId = C.contributorId and D.retrievedInputIdentity = C.retrievedInputIdentity return all D) > 1) return all C))
  else if Count(candidates) = 0 then "__CRL_PublicationSelection_v1_Result"('missing', null, conceptId, null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>)
  else if Count(candidates) = 1 then "__CRL_PublicationSelection_v1_Result"('selected', null, conceptId, singleton from candidates, {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>)
  else if exists (candidates C where C.validity is null return all C) then
    "__CRL_PublicationSelection_v1_Fail"('publication-undated-input', conceptId, (candidates C where C.validity is null return all C))
  else "__CRL_PublicationSelection_v1_Latest"(candidates, conceptId, equalTime)

define function "__CRL_PublicationSelection_v1_Record"(result Tuple { state System.String, failureCode System.String, failureMessage System.String, conceptId System.String, selected Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, affected List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }> }):
  if result.state = 'failed' then
    Message(null as FHIR.Observation, true, result.failureCode, 'Error', result.failureMessage)
  else if result.state = 'selected' then result.selected.resource
  else null as FHIR.Observation


/* REFACTOR:grounded (#320, review 560): observable invalid choices fail before casting. */
define function "__CRL_PublicationSelection_v1_NativeValidity"(D System.DateTime):
  if D is null then null as System.String
  else if (hour from D) is null then ToString(D)
  else if (second from D) is null then
    Message(null as System.String, true, 'publication-incomparable-validity', 'Error', 'A time component requires complete seconds')
  else ToString(DateTime(year from D, month from D, day from D,
    hour from D, minute from D, second from D,
    Coalesce(millisecond from D, 0), timezoneoffset from D))

define function "__CRL_PublicationSelection_v1_LocalBooleanCandidate"(O FHIR.Observation, contributorId System.String, conceptId System.String):
  if O.status.value is null or not (O.status.value in { 'registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown' }) then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-invalid-status', 'Error', conceptId + ': Expected a present, valid FHIR Observation status')
  else if O.status.value in { 'entered-in-error', 'cancelled' } then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-invalidated-record', 'Error', conceptId + ': Explicitly invalidated or cancelled candidates need an authored eligibility policy')
  else if O.value is not null and not (O.value is FHIR.boolean) then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-invalid-value', 'Error', conceptId + ': A present answer must be a FHIR boolean; absence remains unknown')
  else if O.effective is not null and not (O.effective is FHIR.dateTime) then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-invalid-validity-choice', 'Error', conceptId + ': This publication accepts effectiveDateTime or absent validity')
  else Tuple {
    key: if O.id.value is null or O.id.value = '' then 'Observation/<missing-id>' else 'Observation/' + O.id.value,
    contributorId: contributorId,
    arm: 'local',
    retrievedInputIdentity: if O.id.value is null or O.id.value = '' then null as System.String else 'Observation/' + O.id.value,
    resource: O,
    validity: "__CRL_PublicationSelection_v1_NativeValidity"((O.effective as FHIR.dateTime).value)
  }

define function "__CRL_PublicationSelection_v1_LocalCodeableCandidate"(O FHIR.Observation, contributorId System.String, conceptId System.String):
  if O.status.value is null or not (O.status.value in { 'registered', 'preliminary', 'final', 'amended', 'corrected', 'cancelled', 'entered-in-error', 'unknown' }) then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-invalid-status', 'Error', conceptId + ': Expected a present, valid FHIR Observation status')
  else if O.status.value in { 'entered-in-error', 'cancelled' } then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-invalidated-record', 'Error', conceptId + ': Explicitly invalidated or cancelled candidates need an authored eligibility policy')
  else if O.value is not null and not (O.value is FHIR.CodeableConcept) then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-invalid-value', 'Error', conceptId + ': A present answer must be a FHIR CodeableConcept; absence remains unknown')
  else if O.effective is not null and not (O.effective is FHIR.dateTime) then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-invalid-validity-choice', 'Error', conceptId + ': This publication accepts effectiveDateTime or absent validity')
  else Tuple {
    key: if O.id.value is null or O.id.value = '' then 'Observation/<missing-id>' else 'Observation/' + O.id.value,
    contributorId: contributorId,
    arm: 'local',
    retrievedInputIdentity: if O.id.value is null or O.id.value = '' then null as System.String else 'Observation/' + O.id.value,
    resource: O,
    validity: "__CRL_PublicationSelection_v1_NativeValidity"((O.effective as FHIR.dateTime).value)
  }

/* REFACTOR:grounded (#320, review 564): explicit supported source state; no exclusion or false fallback. */
define function "__CRL_PublicationSelection_v1_ServiceRequestCandidate"(S FHIR.ServiceRequest, contributorId System.String,
  conceptId System.String, code FHIR.CodeableConcept, profile System.String, subjectReference System.String):
  if S.status.value is null or S.status.value != 'active' or S.intent.value is null or S.intent.value != 'order'
    or S.doNotPerform.value = true or (S.doNotPerform is not null and S.doNotPerform.value is null)
    or exists(S.modifierExtension) then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-source-state-unsupported', 'Error', conceptId + ': This source projection supports active order requests without prohibition or modifier extensions; other states need an authored eligibility policy')
  else if subjectReference is null or S.subject.reference.value is null
    or not Matches(S.subject.reference.value, '\\A(https?://[^?#]+/)?Patient/[A-Za-z0-9.-]{1,64}(/_history/[A-Za-z0-9.-]{1,64})?\\z')
    or ('Patient/' + Last(Split(
      if PositionOf('/_history/', S.subject.reference.value) >= 0
        then Substring(S.subject.reference.value, 0, PositionOf('/_history/', S.subject.reference.value))
        else S.subject.reference.value, '/'))) != subjectReference then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-source-subject-unsupported', 'Error', conceptId + ': The source must resolve to the current evaluation Patient')
  else if S.id.value is null or not Matches(S.id.value, '\\A[A-Za-z0-9.-]{1,64}\\z') then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-missing-input-identity', 'Error', conceptId + ': A retrieved ServiceRequest requires a valid FHIR id in this dataset')
  else if profile is null then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-source-profile-required', 'Error', conceptId + ': A source-produced Case Feature requires its profile')
  else Tuple {
    key: ToString(Length(contributorId)) + ':' + contributorId + ToString(Length('ServiceRequest/' + S.id.value)) + ':' + 'ServiceRequest/' + S.id.value,
    contributorId: contributorId, arm: 'source', retrievedInputIdentity: 'ServiceRequest/' + S.id.value,
    resource: FHIR.Observation {
      status: FHIR.ObservationStatus { value: 'final' },
      subject: FHIR.Reference { reference: FHIR.string { value: subjectReference } },
      meta: FHIR.Meta { profile: { FHIR.canonical { value: profile } } },
      code: code, value: FHIR.boolean { value: true }, effective: S.authoredOn
    },
    validity: "__CRL_PublicationSelection_v1_NativeValidity"(S.authoredOn.value)
  }

define function "__CRL_PublicationSelection_v1_ObservationCodeableCandidate"(S FHIR.Observation, contributorId System.String,
  conceptId System.String, code FHIR.CodeableConcept, profile System.String, subjectReference System.String):
  if exists(S.modifierExtension) then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-source-state-unsupported', 'Error', 'Observation modifier extensions require an explicit interpretation')
  else if subjectReference is null or S.subject.reference.value is null
    or not Matches(S.subject.reference.value, '\\A(https?://[^?#]+/)?Patient/[A-Za-z0-9.-]{1,64}(/_history/[A-Za-z0-9.-]{1,64})?\\z')
    or ('Patient/' + Last(Split(
      if PositionOf('/_history/', S.subject.reference.value) >= 0
        then Substring(S.subject.reference.value, 0, PositionOf('/_history/', S.subject.reference.value))
        else S.subject.reference.value, '/'))) != subjectReference then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-source-subject-unsupported', 'Error', 'The source must resolve to the current evaluation Patient')
  else if S.id.value is null or not Matches(S.id.value, '\\A[A-Za-z0-9.-]{1,64}\\z') then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, 'publication-missing-input-identity', 'Error', 'A retrieved Observation requires a valid FHIR id')
  else if "__CRL_PublicationSelection_v1_LocalCodeableCandidate"(S, contributorId, conceptId).resource is null then
    null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }
  else Tuple {
    key: ToString(Length(contributorId)) + ':' + contributorId + ToString(Length('Observation/' + S.id.value)) + ':' + 'Observation/' + S.id.value,
    contributorId: contributorId, arm: 'source', retrievedInputIdentity: 'Observation/' + S.id.value,
    resource: FHIR.Observation {
      status: FHIR.ObservationStatus { value: 'final' },
      subject: FHIR.Reference { reference: FHIR.string { value: subjectReference } },
      meta: if profile is null then null as FHIR.Meta else FHIR.Meta { profile: { FHIR.canonical { value: profile } } },
      code: code, value: S.value as FHIR.CodeableConcept, effective: S.effective as FHIR.dateTime,
      derivedFrom: { FHIR.Reference { reference: FHIR.string { value: 'Observation/' + S.id.value } } }
    },
    validity: "__CRL_PublicationSelection_v1_NativeValidity"((S.effective as FHIR.dateTime).value)
  }

/* REFACTOR:grounded (#320, review 562): unary membership consumes the selected operand envelope. */
define function "__CRL_PublicationProducer_v1_ConstructBoolean"(code FHIR.CodeableConcept, datum System.Boolean, profile System.String, operand FHIR.Observation, subjectReference System.String):
  if subjectReference is null or subjectReference = '' then
    Message(null as FHIR.Observation, true, 'publication-missing-subject', 'Error', 'A produced Observation requires an evaluation subject')
  else FHIR.Observation {
    status: FHIR.ObservationStatus { value: 'final' },
    code: code,
    value: if datum is null then null as FHIR.boolean else FHIR.boolean { value: datum },
    subject: FHIR.Reference { reference: FHIR.string { value: subjectReference } },
    meta: if profile is null then null as FHIR.Meta else FHIR.Meta { profile: { FHIR.canonical { value: profile } } },
    effective: operand.effective as FHIR.dateTime,
    derivedFrom: if operand.id.value is null or not Matches(operand.id.value, '^[A-Za-z0-9.-]{1,64}$') then {} as List<FHIR.Reference>
      else { FHIR.Reference { reference: FHIR.string { value: 'Observation/' + operand.id.value } } }
  }

define function "__CRL_PublicationProducer_v1_Recognized"(value FHIR.CodeableConcept, domain List<Tuple { system System.String, code System.String }>):
  value.coding C where exists (domain D where D.system = C.system.value and D.code = C.code.value)

define function "__CRL_PublicationProducer_v1_Interpret"(publication Tuple { state System.String, failureCode System.String, failureMessage System.String, conceptId System.String, selected Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, affected List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }> }, domain List<Tuple { system System.String, code System.String }>):
  if publication.state != 'selected' or publication.selected.resource.value is null then publication
  else if exists ("__CRL_PublicationProducer_v1_Recognized"(publication.selected.resource.value as FHIR.CodeableConcept, domain)) then publication
  else "__CRL_PublicationSelection_v1_Fail"('publication-uninterpretable-value', publication.conceptId, { publication.selected })

/* Interpret is the selected operand's domain authority. This repeated check protects the
   compiler helper invariant when Candidate/Classify receives a direct or foreign envelope. */
define function "__CRL_PublicationProducer_v1_Classify"(value FHIR.CodeableConcept, domain List<Tuple { system System.String, code System.String }>, qualifying List<Tuple { system System.String, code System.String }>, conceptId System.String):
  if value is null then null as System.Boolean
  else if not exists (from ((value).coding) C where exists ((domain) D where D.system = C.system.value and D.code = C.code.value)) then
    Message(null as System.Boolean, true, 'publication-uninterpretable-value', 'Error', conceptId + ': No recognized domain coding')
  else if exists (from ((value).coding) C where exists ((domain) D where D.system = C.system.value and D.code = C.code.value) and exists ((qualifying) Q where Q.system = C.system.value and Q.code = C.code.value)) and exists (from ((value).coding) C where exists ((domain) D where D.system = C.system.value and D.code = C.code.value) and not exists ((qualifying) Q where Q.system = C.system.value and Q.code = C.code.value)) then
    Message(null as System.Boolean, true, 'publication-ambiguous-coded-value', 'Error', conceptId + ': Recognized codings disagree')
  else exists (from ((value).coding) C where exists ((domain) D where D.system = C.system.value and D.code = C.code.value) and exists ((qualifying) Q where Q.system = C.system.value and Q.code = C.code.value))

define function "__CRL_PublicationProducer_v1_Candidate"(operand Tuple { state System.String, failureCode System.String, failureMessage System.String, conceptId System.String, selected Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, affected List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }> }, producerId System.String, code FHIR.CodeableConcept,
  profile System.String, domain List<Tuple { system System.String, code System.String }>, qualifying List<Tuple { system System.String, code System.String }>, conceptId System.String, subjectReference System.String):
  if operand.state = 'failed' then
    Message(null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }, true, operand.failureCode, 'Error', operand.failureMessage)
  else if operand.state != 'selected' then null as Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }
  else Tuple {
    key: ToString(Length(producerId)) + ':' + producerId + ToString(Length(operand.selected.key)) + ':' + operand.selected.key,
    contributorId: producerId,
    arm: 'inferred',
    retrievedInputIdentity: null as System.String,
    resource: "__CRL_PublicationProducer_v1_ConstructBoolean"(code, "__CRL_PublicationProducer_v1_Classify"(operand.selected.resource.value as FHIR.CodeableConcept, domain, qualifying, conceptId), profile, operand.selected.resource, subjectReference),
    validity: operand.selected.validity
  }

define "Diagnosis Records":
  [Condition: "Invasive Breast Carcinoma"]

define "Active Breast Cancer":
  CRLCommon.Active("Diagnosis Records")

define "Indexed Breast Cancer":
  CRLCommon.IsVerified("Active Breast Cancer")

define "Has Active Confirmed Invasive Breast Cancer":
  exists ("Indexed Breast Cancer")

define "__CRL_PublicationEnvelope_v1_Estrogen Receptor Result":
  "__CRL_PublicationProducer_v1_Interpret"("__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (("Estrogen Receptor Result Source 1") S return all "__CRL_PublicationSelection_v1_ObservationCodeableCandidate"(S, 'crl:source:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Estrogen%20Receptor%20Result%22%2C%5B%22source%22%2C0%5D%5D', 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Estrogen%20Receptor%20Result%22%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Estrogen Receptor Result' } }, null as System.String, 'Patient/' + Patient.id.value)) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Estrogen%20Receptor%20Result%22%5D', 'error'), { Tuple { system: 'http://loinc.org', code: 'LA6576-8' }, Tuple { system: 'http://loinc.org', code: 'LA6577-6' } })

define "Estrogen Receptor Result":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Estrogen Receptor Result")

define "__CRL_PublicationEnvelope_v1_Estrogen Receptor Negative":
  "__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (({ "__CRL_PublicationProducer_v1_Candidate"("__CRL_PublicationEnvelope_v1_Estrogen Receptor Result", 'crl:producer:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Estrogen%20Receptor%20Negative%22%2C%5B%22membership%22%2C0%5D%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Estrogen Receptor Negative' } }, null as System.String, { Tuple { system: 'http://loinc.org', code: 'LA6576-8' }, Tuple { system: 'http://loinc.org', code: 'LA6577-6' } }, { Tuple { system: 'http://loinc.org', code: 'LA6577-6' } }, 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Estrogen%20Receptor%20Negative%22%5D', 'Patient/' + Patient.id.value) }) C where C is not null) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Estrogen%20Receptor%20Negative%22%5D', 'error')

define "Estrogen Receptor Negative":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Estrogen Receptor Negative")

define "__CRL_PublicationEnvelope_v1_Progesterone Receptor Result":
  "__CRL_PublicationProducer_v1_Interpret"("__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (("Progesterone Receptor Result Source 1") S return all "__CRL_PublicationSelection_v1_ObservationCodeableCandidate"(S, 'crl:source:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Progesterone%20Receptor%20Result%22%2C%5B%22source%22%2C0%5D%5D', 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Progesterone%20Receptor%20Result%22%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Progesterone Receptor Result' } }, null as System.String, 'Patient/' + Patient.id.value)) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Progesterone%20Receptor%20Result%22%5D', 'error'), { Tuple { system: 'http://loinc.org', code: 'LA6576-8' }, Tuple { system: 'http://loinc.org', code: 'LA6577-6' } })

define "Progesterone Receptor Result":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Progesterone Receptor Result")

define "__CRL_PublicationEnvelope_v1_Progesterone Receptor Negative":
  "__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (({ "__CRL_PublicationProducer_v1_Candidate"("__CRL_PublicationEnvelope_v1_Progesterone Receptor Result", 'crl:producer:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Progesterone%20Receptor%20Negative%22%2C%5B%22membership%22%2C0%5D%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Progesterone Receptor Negative' } }, null as System.String, { Tuple { system: 'http://loinc.org', code: 'LA6576-8' }, Tuple { system: 'http://loinc.org', code: 'LA6577-6' } }, { Tuple { system: 'http://loinc.org', code: 'LA6577-6' } }, 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Progesterone%20Receptor%20Negative%22%5D', 'Patient/' + Patient.id.value) }) C where C is not null) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Progesterone%20Receptor%20Negative%22%5D', 'error')

define "Progesterone Receptor Negative":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Progesterone Receptor Negative")

define "__CRL_PublicationEnvelope_v1_HER2 Result":
  "__CRL_PublicationProducer_v1_Interpret"("__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (("HER2 Result Source 1") S return all "__CRL_PublicationSelection_v1_ObservationCodeableCandidate"(S, 'crl:source:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22HER2%20Result%22%2C%5B%22source%22%2C0%5D%5D', 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22HER2%20Result%22%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'HER2 Result' } }, null as System.String, 'Patient/' + Patient.id.value)) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22HER2%20Result%22%5D', 'error'), { Tuple { system: 'http://loinc.org', code: 'LA6576-8' }, Tuple { system: 'http://loinc.org', code: 'LA6577-6' } })

define "HER2 Result":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_HER2 Result")

define "__CRL_PublicationEnvelope_v1_HER2 Negative":
  "__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (({ "__CRL_PublicationProducer_v1_Candidate"("__CRL_PublicationEnvelope_v1_HER2 Result", 'crl:producer:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22HER2%20Negative%22%2C%5B%22membership%22%2C0%5D%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'HER2 Negative' } }, null as System.String, { Tuple { system: 'http://loinc.org', code: 'LA6576-8' }, Tuple { system: 'http://loinc.org', code: 'LA6577-6' } }, { Tuple { system: 'http://loinc.org', code: 'LA6577-6' } }, 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22HER2%20Negative%22%5D', 'Patient/' + Patient.id.value) }) C where C is not null) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22HER2%20Negative%22%5D', 'error')

define "HER2 Negative":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_HER2 Negative")

define "__CRL_PublicationEnvelope_v1_Clinical M Result":
  "__CRL_PublicationProducer_v1_Interpret"("__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (("Clinical M Result Source 1") S return all "__CRL_PublicationSelection_v1_ObservationCodeableCandidate"(S, 'crl:source:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20M%20Result%22%2C%5B%22source%22%2C0%5D%5D', 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20M%20Result%22%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Clinical M Result' } }, null as System.String, 'Patient/' + Patient.id.value)) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20M%20Result%22%5D', 'error'), { Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cM0' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cM1' } })

define "Clinical M Result":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Clinical M Result")

define "__CRL_PublicationEnvelope_v1_Nonmetastatic Disease Result":
  "__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (({ "__CRL_PublicationProducer_v1_Candidate"("__CRL_PublicationEnvelope_v1_Clinical M Result", 'crl:producer:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Nonmetastatic%20Disease%20Result%22%2C%5B%22membership%22%2C0%5D%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Nonmetastatic Disease Result' } }, null as System.String, { Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cM0' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cM1' } }, { Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cM0' } }, 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Nonmetastatic%20Disease%20Result%22%5D', 'Patient/' + Patient.id.value) }) C where C is not null) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Nonmetastatic%20Disease%20Result%22%5D', 'error')

define "Nonmetastatic Disease Result":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Nonmetastatic Disease Result")

define "__CRL_PublicationEnvelope_v1_Clinical N Result":
  "__CRL_PublicationProducer_v1_Interpret"("__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (("Clinical N Result Source 1") S return all "__CRL_PublicationSelection_v1_ObservationCodeableCandidate"(S, 'crl:source:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20N%20Result%22%2C%5B%22source%22%2C0%5D%5D', 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20N%20Result%22%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Clinical N Result' } }, null as System.String, 'Patient/' + Patient.id.value)) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20N%20Result%22%5D', 'error'), { Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN0' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN1' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN2' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN3' } })

define "Clinical N Result":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Clinical N Result")

define "__CRL_PublicationEnvelope_v1_Clinically Positive Nodes Result":
  "__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (({ "__CRL_PublicationProducer_v1_Candidate"("__CRL_PublicationEnvelope_v1_Clinical N Result", 'crl:producer:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinically%20Positive%20Nodes%20Result%22%2C%5B%22membership%22%2C0%5D%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Clinically Positive Nodes Result' } }, null as System.String, { Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN0' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN1' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN2' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN3' } }, { Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN1' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN2' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cN3' } }, 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinically%20Positive%20Nodes%20Result%22%5D', 'Patient/' + Patient.id.value) }) C where C is not null) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinically%20Positive%20Nodes%20Result%22%5D', 'error')

define "Clinically Positive Nodes Result":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Clinically Positive Nodes Result")

define "__CRL_PublicationEnvelope_v1_Clinical T Result":
  "__CRL_PublicationProducer_v1_Interpret"("__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (("Clinical T Result Source 1") S return all "__CRL_PublicationSelection_v1_ObservationCodeableCandidate"(S, 'crl:source:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20T%20Result%22%2C%5B%22source%22%2C0%5D%5D', 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20T%20Result%22%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Clinical T Result' } }, null as System.String, 'Patient/' + Patient.id.value)) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20T%20Result%22%5D', 'error'), { Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT1a' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT1b' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT1c' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT1mi' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT2' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT3' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT4' } })

define "Clinical T Result":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Clinical T Result")

define "__CRL_PublicationEnvelope_v1_Clinical T1c Or Higher Result":
  "__CRL_PublicationSelection_v1_Select"(Flatten({ {} as List<Tuple { key System.String, contributorId System.String, arm System.String, retrievedInputIdentity System.String, resource FHIR.Observation, validity System.String }>, (({ "__CRL_PublicationProducer_v1_Candidate"("__CRL_PublicationEnvelope_v1_Clinical T Result", 'crl:producer:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20T1c%20Or%20Higher%20Result%22%2C%5B%22membership%22%2C0%5D%5D', FHIR.CodeableConcept { text: FHIR.string { value: 'Clinical T1c Or Higher Result' } }, null as System.String, { Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT1a' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT1b' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT1c' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT1mi' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT2' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT3' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT4' } }, { Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT1c' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT2' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT3' }, Tuple { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'cT4' } }, 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20T1c%20Or%20Higher%20Result%22%5D', 'Patient/' + Patient.id.value) }) C where C is not null) }), 'crl:concept:v1:%5B%22https%3A%2F%2Falphora.github.io%2Fhl7-agentic-knowledge-connectathon%2Ffhir%22%2C%22breast-cancer-neoadjuvant%22%2C%22Breast%20Cancer%20Neoadjuvant%22%2C%22breast-cancer-neoadjuvant%22%2C%220.0.0%22%2C%22Clinical%20T1c%20Or%20Higher%20Result%22%5D', 'error')

define "Clinical T1c Or Higher Result":
  "__CRL_PublicationSelection_v1_Record"("__CRL_PublicationEnvelope_v1_Clinical T1c Or Higher Result")

define "Estrogen Receptor Result Source 1":
  [Observation: { System.Code { system: 'http://loinc.org', code: '85337-4' } }]

define "Progesterone Receptor Result Source 1":
  [Observation: { System.Code { system: 'http://loinc.org', code: '85339-0' } }]

define "HER2 Result Source 1":
  [Observation: { System.Code { system: 'http://loinc.org', code: '48676-1' } }]

define "Clinical M Result Source 1":
  [Observation: { System.Code { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'clinical-m' } }]

define "Clinical N Result Source 1":
  [Observation: { System.Code { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'clinical-n' } }]

define "Clinical T Result Source 1":
  [Observation: { System.Code { system: 'https://reason-healthcare.github.io/hl7-agentic-knowledge-connectathon/fhir/CodeSystem/breast-cancer-fixture', code: 'clinical-t' } }]

define "Has Nonmetastatic Disease":
  FHIRHelpers.ToBoolean(("Nonmetastatic Disease Result").value as FHIR.boolean)

define "Has Clinically Positive Nodes":
  FHIRHelpers.ToBoolean(("Clinically Positive Nodes Result").value as FHIR.boolean)

define "Has Clinical T1c Or Higher":
  FHIRHelpers.ToBoolean(("Clinical T1c Or Higher Result").value as FHIR.boolean)

define "In Neoadjuvant Review Population":
  "Has Active Confirmed Invasive Breast Cancer" and "Has Nonmetastatic Disease"

define "Is Triple Negative":
  FHIRHelpers.ToBoolean(("Estrogen Receptor Negative").value as FHIR.boolean) and FHIRHelpers.ToBoolean(("Progesterone Receptor Negative").value as FHIR.boolean) and FHIRHelpers.ToBoolean(("HER2 Negative").value as FHIR.boolean)

define "Meets Tumor Or Node Criterion":
  "Has Clinical T1c Or Higher" or "Has Clinically Positive Nodes"

define "Neoadjuvant TNBC Guidance Applicable":
  "In Neoadjuvant Review Population" and "Is Triple Negative" and "Meets Tumor Or Node Criterion"

define "CRL branch CriterionRef L169C7":
  "Neoadjuvant TNBC Guidance Applicable"

define "Not CRL branch CriterionRef L169C7":
  not ("Neoadjuvant TNBC Guidance Applicable")
