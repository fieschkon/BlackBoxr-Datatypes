from BBData.BBData import *
from BBData.Fields import *
class FieldTemplates:
    FeatureFields = [
        Enum(['Electrical Feature', 'Mechanical Feature', 'Firmware Feature', 'Software Feature'], ['Electrical Feature']),
        LongText('Description'),
        ShortText('Production Cost Estimate')
    ]

    RequirementFields = [
        LongText('Requirement'),
        LongText('Rationale'),
        Enum(['Electrical Engineer', 'Software Engineer', 'Mechanical Engineer'], 'Electrical Engineer', 'Assigned To')
    ]

    TestCaseFields = [
        LongText('Preconditions'),
        LongText('Procedure'),
        LongText('Pass Conditions')
    ]

class Definitions:

    Folder = WorkItemDefinition(name='Folder')

    Feature = WorkItemDefinition(name='Feature')
    Requirement = WorkItemDefinition(name='Requirement')
    TestCase = WorkItemDefinition(name='Test Case')

    Feature.addDownstreamRule(Requirement)
    Requirement.addDownstreamRule(TestCase)

    Feature.addPublicFields(FieldTemplates.FeatureFields)
    Requirement.addPublicFields(FieldTemplates.RequirementFields)
    Feature.addPublicFields(FieldTemplates.TestCaseFields)