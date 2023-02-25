import os
from random import randint
import random
import string
from BBData.BBData import WorkItem, WorkItemDefinition, Scope
from BBData.Fields import *

currentworkspace = Scope.setCurrentWorkspaceFromDirectory(os.path.join(os.getcwd(), 'ex'))

'''
GENERIC PROJECT EXAMPLE
'''
# Make a project
ExampleProject = currentworkspace.createNewProject('Example Project')

'''
Folder definitions
'''
# Make a folder for definitions
DefinitionsFolder = ExampleProject.createNewDocument('Definitions', parent=ExampleProject)

# Make Hardware requirements folder
HWFolder = ExampleProject.createNewDocument('Hardware', parent=ExampleProject)
# And some subfolders for organizational purposes
SystemRequirements = ExampleProject.createNewDocument('System Requirements', parent=HWFolder)
SubSystemRequirements = ExampleProject.createNewDocument('Sub-system Requirements', parent=HWFolder)

'''
Defining definitions
'''
# Make definitions and add them to the definitions folder
SystemRequirementDefinition = ExampleProject.createWorkItemDefinition(parent=DefinitionsFolder)
SubsystemRequirementDefinition = ExampleProject.createWorkItemDefinition(parent=DefinitionsFolder)

# Set rule to allow subsystem type downstream of system
SystemRequirementDefinition.addDownstreamRule(SubsystemRequirementDefinition)

# Define requirement fields
RequirementFields = [
    LongText('Requirement'),
    Enum(['Electrical Engineer', 'Software Engineer', 'Mechanical Engineer'], 'Electrical Engineer', 'Assigned To')
]

# Add fields to definitions
SystemRequirementDefinition.addPublicFields(RequirementFields)
SubsystemRequirementDefinition.addPublicFields(RequirementFields)

'''
Create Requirements
'''
StartupTime = ExampleProject.createWorkItem('Shutdown Time', SystemRequirementDefinition, SystemRequirements)
StartupTime.getPublicField('Requirement').setText('The system shall have a shutdown time of no more than 500 ns.')
StartupTime.getPublicField('Assigned To').setCurrent('Electrical Engineer')

CapSize = ExampleProject.createWorkItem('Cap Size', SubsystemRequirementDefinition, SubSystemRequirements)
CapSize.getPublicField('Requirement').setText('The regulator output shall have an input capacitance no larger than 10 uF.')
CapSize.getPublicField('Assigned To').setCurrent('Electrical Engineer')

StartupTime.addDownstream(CapSize)
'''
STANDARD EXAMPLE
'''
# Make Standard
StandardsFolder = currentworkspace.createNewDocument('Standards')
iso_6469 = currentworkspace.createNewProject('ISO-6469', StandardsFolder)
Substandard = iso_6469.createNewDocument('3')

currentworkspace.print()