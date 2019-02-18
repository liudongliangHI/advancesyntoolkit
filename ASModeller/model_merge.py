'''
Functions to merge several sets of model objects into a single 
set of model objects.

Date created: 17th February 2019

This file is part of AdvanceSyn Modeller, which is a part of 
AdvanceSyn ToolKit.

Copyright (c) 2018, AdvanceSyn Private Limited.

Licensed under the Apache License, Version 2.0 (the "License") for 
academic and not-for-profit use only; commercial and/or for profit 
use(s) is/are not licensed under the License and requires a 
separate commercial license from the copyright owner (AdvanceSyn 
Private Limited); you may not use this file except in compliance 
with the License. You may obtain a copy of the License at 
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

def _renumberReactions(modelnumber, count, 
                       spec, modelobj,
                       p_spec=True, p_modelobj=True):
    if p_spec:
        print('Renaming / Renumbering Reactions in Specification ' + \
            str(modelnumber))
        table = {}
        # Step 1: Generate reaction renumbering table
        for rxn_ID in spec['Reactions']:
            table[rxn_ID] = 'exp' + str(count)
            count = count + 1
        # Step 2: Renumber specification
        for rxn_ID in spec['Reactions']:
            newID = table[rxn_ID]
            spec['Reactions'][newID] = spec['Reactions'][rxn_ID]
            del spec['Reactions'][rxn_ID]
            print('  Specification %s: %s --> %s' % \
                (modelnumber, rxn_ID, newID))
        print('')
    if p_modelobj:
    # Step 3: Renumbering model objects
        print('  Number of Model Objects in Specification %s: %s' \
            % (modelnumber, len(modelobj)))
        print('')
        index = 1
        for name in modelobj:
            mobj = modelobj[name]
            print('  Object Name / Description %s: %s | %s' % \
                (index, mobj.name, mobj.description))
            print('')
            index = index + 1
            for key in list(mobj.influx.keys()):
                newID = table[key]
                mobj.influx[newID] = mobj.influx[key]
                del mobj.influx[key]
                print('    Influx %s --> %s' % (key, newID))
            for key in list(mobj.outflux.keys()):
                newID = table[key]
                mobj.outflux[newID] = mobj.outflux[key]
                del mobj.outflux[key]
                print('    Outflux %s --> %s' % (key, newID))
            print('')
    '''
    for key in spec['Reactions']:
        print('%s / %s' % (key, spec['Reactions'][key]))
    '''
    return (spec, modelobj, count)

def renameReactions(specList, modelobjList,
                    p_specList=True, p_modelobjList=True):
    count = 1
    for index in range(len(specList)):
        (spec, 
         modelobj,
         count) = _renumberReactions(index+1, count,
                                     specList[index], 
                                     modelobjList[index],
                                     p_specList, 
                                     p_modelobjList)
        specList[index] = spec
        modelobjList[index] = modelobj
    return (specList, modelobjList)

def mergeSpecification(spec, specList):
    print('Merge Specifications ...')
    statistics = {'Identifiers': [len(spec['Identifiers'])],
                  'Objects': [len(spec['Objects'])],
                  'Initials': [len(spec['Initials'])],
                  'Variables': [len(spec['Variables'])],
                  'Reactions': [len(spec['Reactions'])]}
    for s in specList:
        # Step 1: Merge identifiers
        for key in s['Identifiers']:
            count = 1
            newkey = key + '_' + str(count)
            spec['Identifiers'][newkey] = s['Identifiers'][key]
            count = count + 1
        number = len(s['Identifiers'])
        statistics['Identifiers'].append(number)
        # Step 2: Merge objects
        for key in s['Objects']:
            spec['Objects'][key] = s['Objects'][key]
        number = len(s['Objects'])
        statistics['Objects'].append(number)
        # Step 3: Merge initials
        for key in s['Initials']:
            spec['Initials'][key] = s['Initials'][key]
        number = len(s['Initials'])
        statistics['Initials'].append(number)
        # Step 4: Merge variables
        for key in s['Variables']:
            spec['Variables'][key] = s['Variables'][key]
        number = len(s['Variables'])
        statistics['Variables'].append(number)
        # Step 5: Merge reactions
        for key in s['Reactions']:
            spec['Reactions'][key] = s['Reactions'][key]
        number = len(s['Reactions'])
        statistics['Reactions'].append(number)
    '''
    for stanza in spec:
        for key in spec[stanza]:
            print('%s / %s / %s' % \
                  (stanza, key, spec[stanza][key]))
    '''
    print('Numbers of Identifiers = %s' % \
        ', '.join([str(x) for x in statistics['Identifiers']]))
    print('... Total Numbers of Identifiers = %s' % \
        str(sum(statistics['Identifiers'])))
    print('Numbers of Objects = %s' % \
        ', '.join([str(x) for x in statistics['Objects']]))
    print('... Total Numbers of Objects = %s' % \
        str(sum(statistics['Objects'])))
    print('Numbers of Initials = %s' % \
        ', '.join([str(x) for x in statistics['Initials']]))
    print('... Total Numbers of Initials = %s' % \
        str(sum(statistics['Initials'])))
    print('Numbers of Variables = %s' % \
        ', '.join([str(x) for x in statistics['Variables']]))
    print('... Total Numbers of Variables = %s' % \
        str(sum(statistics['Variables'])))
    print('Numbers of Reactions = %s' % \
        ', '.join([str(x) for x in statistics['Reactions']]))
    print('... Total Numbers of Reactions = %s' % \
        str(sum(statistics['Reactions'])))
    print('')
    return spec

def mergeModelObjects(modelobj, modelobjList):
    print('Merging Model Objects ...')
    objcount = [len(modelobj)] + [len(x) for x in modelobjList]
    print('Number of Model Objects: %s' % \
        ', '.join([str(x) for x in objcount]))
    print('... Total Numbers of Model Objects = %s' % \
        str(sum(objcount)))
    print('')
    objectNames = list(modelobj.keys())
    spec_count = 1
    print('  Names of Model Objects from Specification %s: %s' \
        % (spec_count, ' | '.join(objectNames)))
    print('')
    for mobjs in modelobjList:
        print('  Number of Merged Model Objects: %s' \
        % len(objectNames))
        print('  Current Names of Merged Model Objects: %s' \
        % ' | '.join(objectNames))
        print('')
        spec_count = spec_count + 1
        print('  Names of Model Objects from Specification %s: %s' \
            % (spec_count, ' | '.join(list(mobjs.keys()))))
        print('')
        for name in mobjs:
            if name not in objectNames:
                print('    %s object is not in current merged list - full model object merge' \
                    % name)
                modelobj[name] = mobjs[name]
                objectNames.append(name)
            else:
                print('    %s object is in current merged list - merge fluxes' \
                    % name)
                cobj = modelobj[name]
                c_in = [cobj.influx[k] for k in cobj.influx]
                c_out = [cobj.outflux[k] for k in cobj.outflux]
                nobj = mobjs[name]
                for k in nobj.influx:
                    if nobj.influx[k] not in c_in:
                        print('    Influx (%s) in %s is not present in current object - influx merged' \
                            % (nobj.influx[k], name))
                        cobj.influx[k] = nobj.influx[k]
                    else:
                        print('    Influx (%s) in %s is already present in current object - influx not merged' \
                            % (nobj.influx[k], name))
                for k in nobj.outflux:
                    if nobj.outflux[k] not in c_out:
                        print('    Outflux (%s) in %s is not present in current object - outflux merged' \
                            % (nobj.outflux[k], name))
                        cobj.outflux[k] = nobj.outflux[k]
                    else:
                        print('    Outflux (%s) in %s is already present in current object - outflux not merged' \
                            % (nobj.outflux[k], name))
        print('')
    print('  Number of Merged Model Objects: %s' % \
        len(objectNames))
    print('  Current Names of Merged Model Objects: %s' % \
        ' | '.join(objectNames))
    print('')
    return modelobj

def modelMerge(specList, modelobjList):
    (specList, modelobjList) = renameReactions(specList, 
                                               modelobjList)
    merged_spec = specList[0]
    merged_modelobj = modelobjList[0]
    specList = specList[1:]
    modelobjList = modelobjList[1:]
    merged_spec = mergeSpecification(merged_spec, specList)
    merged_modelobj = mergeModelObjects(merged_modelobj, 
                                        modelobjList)
    return (merged_spec, merged_modelobj)
