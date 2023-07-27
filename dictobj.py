import json


def removeDictKey(d, k):
    r = dict(d)
    del r[k]
    return r


def listToString(s):
    separator = ','
    return (separator.join(s))


def removeNewLine(s):
    return s.replace('\n', '')


def getDict(doc):
    entries_to_delete = []

    contractName = '' if not 'contractName' in doc else doc['contractName'].translate(
        str.maketrans('', '', '*'))

    matConValue = 0
    if 'matConValue' in doc:
        if type(doc['matConValue']) in (tuple, list):
            matConValue = doc['matConValue'][0]
        else:
            matConValue = doc['matConValue']

        if type(matConValue) == str:
            tmp = matConValue.replace(',', '')
            matConValue = float(tmp)

    origcontractEndDate = None if not 'OrigcontractEndDate' in doc else f'{doc["OrigcontractEndDate"][6:]}-{doc["OrigcontractEndDate"][0:2]}-{doc["OrigcontractEndDate"][3:5]}'

    multiYear = ''
    if 'multiYear' in doc:
        multiYear = 'Yes' if doc['multiYear'] == 'Y' else 'No'

    spaceDelReq = ''
    if 'spaceDelReq' in doc:
        spaceDelReq = 'Yes' if doc['spaceDelReq'] == 'Y' else 'No'

    invReq = ''
    if 'invReq' in doc:
        invReq = 'Yes' if doc['invReq'] == 'Y' else 'No'

    invReqComments = None if not 'invReqComments' in doc else doc['invReqComments'][0:100]

    contractType = ''
    secContractTypeKey = ''
    secContractTypeValue = []
    if 'contractType' in doc:
        switcher = {
            'J': 'GSA',
            'K': 'Special Bid',
            'L': 'Open Market',
            'T': 'Tria'
        }
        contractType = switcher.get(doc['contractType'])

        if doc['contractType'] == 'J':
            switcherGSA = {
                'S1': 'GSA Schedule',
                'S2': 'GSA \'Spot\' Pricing',
                'S3': 'GSA Teaming Agreement',
                'S4': 'GSA Promotion',
                'S5': 'GSA Mixed',
                'S6': 'GSA Blanket Purchase Agreement',
                'S7': 'GSA Enterprise License Agreement'
            }
            secContractTypeKey = 'secondaryContractTypeGSA'
            if not secContractTypeKey in doc:
                secContractTypeKey = 'secContractTypeKey'
                secContractTypeValue = ''
                entries_to_delete.append('secContractTypeKey')
            if type(doc['secondaryContractTypeGSA']) in (tuple, list):
                for value in doc['secondaryContractTypeGSA']:
                    secContractTypeValue.append(
                        {'id': switcherGSA.get(value), 'label': switcherGSA.get(value)})
            else:
                secContractTypeValue.append({'id': switcherGSA.get(
                    doc['secondaryContractTypeGSA']), 'label': switcherGSA.get(doc['secondaryContractTypeGSA'])})
        elif doc['contractType'] == 'K':
            switcherSB = {
                'S10': 'Basic Ordering Agreement',
                'S11': 'Definite Delivery/Definite Quantity',
                'S12': 'Indefinite Delivery/ Indefinite Quantity',
                'S13': 'Botton line bid',
                'S14': 'Enterprise Licence Agreement',
                'S15': 'FSI Agreement',
                'S16': 'BPA',
                'S17': 'Capital Purchase'
            }
            secContractTypeKey = 'secondaryContractTypeSB'
            if not secContractTypeKey in doc:
                secContractTypeKey = 'secContractTypeKey'
                secContractTypeValue = ''
                entries_to_delete.append('secContractTypeKey')
            elif type(doc['secondaryContractTypeSB']) in (tuple, list):
                for value in doc['secondaryContractTypeSB']:
                    secContractTypeValue.append(
                        {'id': switcherSB.get(value), 'label': switcherSB.get(value)})
            else:
                secContractTypeValue.append({'id': switcherSB.get(
                    doc['secondaryContractTypeSB']), 'label': switcherSB.get(doc['secondaryContractTypeSB'])})
        else:
            secContractTypeKey = 'secContractTypeKey'
            secContractTypeValue = ''
            entries_to_delete.append('secContractTypeKey')

    contractTerms = ''
    if not 'contractTerms' in doc:
        contractTerms = 'Standard'
    else:
        contractTerms = 'Non Standard' if doc['contractTerms'] == 'Non-Standard' else 'Standard'

    comp_type_arr = []
    if 'MasConComponType' in doc:
        if type(doc['MasConComponType']) in (tuple, list):
            for value in doc['MasConComponType']:
                comp_type_arr.append({'id': value, 'label': value})
        else:
            comp_type_arr.append(
                {'id': doc['MasConComponType'], 'label': doc['MasConComponType']})
    else:
        comp_type_arr.append({})
        entries_to_delete.append('MasConComponType')

    comp_type_hw_brand_arr = []
    if 'masContHWBrand' in doc:
        if type(doc['masContHWBrand']) in (tuple, list):
            for value in doc['masContHWBrand']:
                comp_type_hw_brand_arr.append({'id': value, 'label': value})
        else:
            comp_type_hw_brand_arr.append(
                {'id': doc['masContHWBrand'], 'label': doc['masContHWBrand']})
    else:
        comp_type_hw_brand_arr.append({})
        entries_to_delete.append('masContHWBrand')

    masContESWsub = ''
    if 'masContESWsub' in doc:
        if doc['masContESWsub'] == 'Y':
            masContESWsub = 'Yes'
        elif doc['masContESWsub'] == 'N':
            masContESWsub = 'No'
        else:
            masContESWsub = ''

    masContESWLic = ''
    if 'masContESWLic' in doc:
        if doc['masContESWLic'] == 'Y':
            masContESWLic = 'Yes'
        elif doc['masContESWLic'] == 'N':
            masContESWLic = 'No'
        else:
            masContESWLic = ''

    masContDSWsub = ''
    if 'masContDSWsub' in doc:
        if doc['masContDSWsub'] == 'Y':
            masContDSWsub = 'Yes'
        elif doc['masContDSWsub'] == 'N':
            masContDSWsub = 'No'
        else:
            masContDSWsub = ''

    capOnDemand = ''
    capOnDemandOpt = None
    if 'CapOnDemand' in doc:
        if doc['CapOnDemand'] == 'Y':
            capOnDemand = 'Yes'
            capOnDemandOpt = []
            if type(doc['CapOnDemandOpt']) in (tuple, list):
                for value in doc['CapOnDemandOpt']:
                    capOnDemandOpt.append({'id': value, 'label': value})
            else:
                capOnDemandOpt.append({
                    'id': doc['CapOnDemandOpt'],
                    'label': doc['CapOnDemandOpt']
                })
        elif doc['CapOnDemand'] == 'N':
            capOnDemand = 'No'
        else:
            capOnDemand = ''

    riskOfLoss = ''
    riskOfLossReason = ''
    if not 'riskOfLoss' in doc:
        riskOfLoss = 'Yes'
    elif doc['riskOfLoss'] == 'N':
        riskOfLoss = 'No'
        switcher = {
            'Acceptance': 'Accepted',
            'Delivery': 'Delivery',
            'Inspection': 'Inspection',
            'Installation': 'Installation',
            'Other (explain)': 'Other (Explain)'
        }
        riskOfLossReason = '' if not 'riskOfLossReason' in doc else switcher.get(
            doc['riskOfLossReason'])
    else:
        riskOfLoss = 'Yes'

    titlePasesToFedGov = ''
    titlePasesToFedGovReasonKey = 'titlePasesToFedGovReason_Yes'
    titlePasesToFedGovReasonValue = ''
    if not 'titlePasesToFedGov' in doc:
        titlePasesToFedGov = 'No'
    elif doc['titlePasesToFedGov'] == 'Y':
        titlePasesToFedGov = 'Yes'
        switcher = {
            'Acceptance': 'Acceptance',
            'Delivery': 'Delivery',
            'Inspection': 'Inspection',
            'Installation': 'Instalation',
            'Payment': 'Payment',
            'Shipment': 'Shipment'
        }
        titlePasesToFedGovReasonKey = 'titlePasesToFedGovReason_Yes'
    else:
        titlePasesToFedGov = 'No'
        switcher = {
            'Prime Contractor': 'Prime Contractor',
            'Federal Systems Integrator': 'Federal Sistem Integrator',
            'Other (explain)': 'Other (Explain)'
        }
        titlePasesToFedGovReasonKey = 'titlePasesToFedGovReason'
    titlePasesToFedGovReasonValue = '' if not titlePasesToFedGovReasonKey in doc else switcher.get(
        doc[titlePasesToFedGovReasonKey])

    futureConting = ''
    if not 'futureConting' in doc:
        futureConting = 'No'
    else:
        futureConting = 'Yes' if doc['futureConting'] == 'Y' else 'No'

    paymentBillp = ''
    if not 'paymentBillp' in doc:
        paymentBillp = 'No'
    else:
        paymentBillp = 'Yes' if doc['paymentBillp'] == 'Y' else 'No'

    multiElementArrangement = ''
    if not 'multiElementArrangement' in doc:
        multiElementArrangement = 'No'
    else:
        multiElementArrangement = 'Yes' if doc['multiElementArrangement'] == 'Y' else 'No'

    otherTermCondition = ''
    if not 'otherTermCondition' in doc:
        otherTermCondition = 'No'
    else:
        otherTermCondition = 'Yes' if doc['otherTermCondition'] == 'Y' else 'No'

    contractProv = ''
    if not 'contractProv' in doc:
        contractProv = 'No'
    else:
        contractProv = 'Yes' if doc['contractProv'] == 'Y' else 'No'

    contractor_type_switcher = {
        'CP': 'Capital Purchase (CP)',
        'FSI': 'Federal Systems Integrator (FSI)',
        'MOC': 'Management and Operating Contract (MOC)',
        'PC': 'Prime Contractor (PC)'
    }
    contractor_type = None if not 'contractorType' in doc else contractor_type_switcher.get(
        doc['contractorType'])

    state_switcher = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington - District of Columbia',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming',
        'AS': 'American Samoa',
        'DC': 'District of Columbia',
        'GU': 'Guam',
        'MH': 'Marshall Islands',
        'MP': 'Northern Mariana Island',
        'PR': 'Puerto Rico',
        'VI': 'Virgin Islands'
    }
    fsi_state = None if not 'fsiState' in doc else state_switcher.get(
        doc['fsiState'])
    contact_state = None if not 'contactState' in doc else state_switcher.get(
        doc['contactState'])

    creditApprovalStatus = ''
    if 'creditApprovalStatus' in doc:
        if doc['creditApprovalStatus'] == 'Y':
            creditApprovalStatus = 'Yes'
        elif doc['creditApprovalStatus'] == 'N':
            creditApprovalStatus = 'No'
        else:
            creditApprovalStatus = ''

    escrowAgreementReceived = ''
    if 'escrowAgreementReceived' in doc:
        if doc['escrowAgreementReceived'] == 'Y':
            escrowAgreementReceived = 'Yes'
        elif doc['escrowAgreementReceived'] == 'N':
            escrowAgreementReceived = 'No'
        else:
            escrowAgreementReceived = ''

    escrowCOD = ''
    if 'escrowCOD' in doc:
        if doc['escrowCOD'] == 'Y':
            escrowCOD = 'Yes'
        elif doc['escrowCOD'] == 'N':
            escrowCOD = 'No'
        else:
            escrowCOD = ''

    reconCycle = ''
    reconScheduleKey = ''
    reconScheduleValue = ''
    if not 'reconCycle' in doc:
        reconCycle = 'Monthly'
        reconScheduleKey = 'reconCycleAnual'
        reconScheduleValue = None
    elif doc['reconCycle'] == 'a':
        reconCycle = 'Anual'
        reconScheduleKey = 'reconCycleAnual'
        switcher = {
            '1a': 'January',
            '2a': 'February',
            '3a': 'March',
            '4a': 'April',
            '5a': 'May',
            '6a': 'June',
            '7a': 'July',
            '8a': 'August',
            '9a': 'September',
            '10a': 'October',
            '11a': 'November',
            '12a': 'December'
        }
        reconScheduleValue = '' if not 'reconSch' in doc else switcher.get(
            doc['reconSch'])
    elif doc['reconCycle'] == 'm':
        reconCycle = 'Monthly'
        reconScheduleKey = 'reconCycleAnual'
        reconScheduleValue = None
    elif doc['reconCycle'] == 'q':
        reconCycle = 'Quarterly'
        reconScheduleKey = 'reconCycleQuarterly'
        switcher = {
            '1q': 'January / April / July / October',
            '2q': 'February / May / August / November',
            '3q': 'March / June / September / December'
        }
        reconScheduleValue = '' if not 'reconSch' in doc else switcher.get(
            doc['reconSch'])
    else:
        reconCycle = 'Semi-Annual'
        reconScheduleKey = 'reconCycleSemiAnual'
        switcher = {
            '1s': 'January / July',
            '2s': 'February / August',
            '3s': 'March / September',
            '4s': 'April / October',
            '5s': 'May / November',
            '6s': 'June / December'
        }
        reconScheduleValue = '' if not 'reconSch' in doc else switcher.get(
            doc['reconSch'])

    types = ['HW', 'LSW', 'DSW', 'ESW', 'SysX',
             'Svsc', 'MA', 'Appl', 'Oth', 'IGF']
    lines = ['', '_1', '_1_1', '_1_2', '_1_3', '_1_4',
             '_1_5', '_1_6', '_1_7', '_1_8', '_1_9', '_1_10']
    fields = ['PoNo', '_Custno', '_Inv_No', '_Inv_Dt',
              '_Inv_Amt', '_Taxes', '_SourceCd', '_Inv_Clr_Dt']
    tswitcher = {
        'HW': 'Hardware',
        'LSW': 'Legacy SW',
        'DSW': 'DSW SW',
        'ESW': 'ESW SW',
        'SysX': 'System X',
        'Svsc': 'Services',
        'MA': 'Annuity Services',
        'Appl': 'Appliances',
        'Oth': 'Other',
        'IGF': 'IGF'
    }
    gstr = ''
    for t in types:
        for l in lines:
            if t + 'PoNo' + l in doc:
                gobj = {
                    'offering': tswitcher.get(t),
                    'poNumber': '' if not t + fields[0] + l in doc else doc[t + fields[0] + l],
                    'customerNumber': '' if not t + fields[1] + l in doc else doc[t + fields[1] + l],
                    'invoiceNumber': '' if not t + fields[2] + l in doc else doc[t + fields[2] + l],
                    'invoiceDate': '' if not t + fields[3] + l in doc else doc[t + fields[3] + l],
                    'invoiceAmount': '' if not t + fields[4] + l in doc else doc[t + fields[4] + l],
                    'taxes': 0 if not t + fields[5] + l in doc else doc[t + fields[5] + l],
                    'sourcesCodes': '' if not t + fields[6] + l in doc else doc[t + fields[6] + l],
                    'invoiceClearedDate': '' if not t + fields[7] + l in doc else doc[t + fields[7] + l]
                }
                if t == 'MA':
                    gobj['quoteId'] = '' if not t + '_ISAT_No' + \
                        l in doc else doc[t + '_ISAT_No' + l]
                else:
                    gobj['quoteId'] = '' if not t + 'QuoteID' + \
                        l in doc else doc[t + 'QuoteID' + l]
                gstr = json.dumps(gobj) if gstr == '' else gstr + \
                    ',' + json.dumps(gobj)
            else:
                break
    offeringGrid = '[' + gstr + ']'
    # offeringGrid = offeringGrid.replace('"', "'")

    mlines = ['', '_1', '_1_1', '_1_2', '_1_3', '_1_4',
              '_1_5', '_1_6', '_1_7', '_1_8', '_1_9', '_1_10']
    mfields = ['PoNo', '_Custno', '_Inv_No', '_Inv_Dt',
               '_Inv_Amt', '_Taxes', '_Inv_Snt_Dt', '_Inv_Clr_Dt']
    mswitcher = {
        'PoNo': 'poNumber',
        '_Custno': 'customerNumber',
        '_Inv_No': 'invoiceNumber',
        '_Inv_Dt': 'invoiceDate',
        '_Inv_Amt': 'invoiceAmount',
        '_Taxes': 'taxes',
        '_Inv_Snt_Dt': 'invoiceSentDate',
        '_Inv_Clr_Dt': 'invoiceClearedDate'
    }

    caca = []
    for l in mlines:
        if 'MBPoNo' + l in doc:

            entry = {}
            for f in mfields:
                # print(f'MB{f}{l}')

                entry_name = mswitcher.get(f)

                if f == '_Inv_Amt' or f == '_Taxes':
                    entry[entry_name] = {
                        'value': 0 if not f'MB{f}{l}' in doc else doc[f'MB{f}{l}']}
                else:
                    entry[entry_name] = {
                        'value': '' if not f'MB{f}{l}' in doc else doc[f'MB{f}{l}']}
        else:
            break

        caca.append(entry)
        # print(caca)

    manualBillingGrid = json.dumps(caca)

    tstr = {}
    if 'HwRevTotal' in doc:
        tstr['Hardware'] = doc['HwRevTotal']
    if 'LSwRevTotal' in doc:
        tstr['Legacy SW'] = doc['LSwRevTotal']
    if 'DSWRevTotal' in doc:
        tstr['DSW SW'] = doc['DSWRevTotal']
    if 'ESWRevTotal' in doc:
        tstr['ESW SW'] = doc['ESWRevTotal']
    if 'SysXRevTotal' in doc:
        tstr['System X'] = doc['SysXRevTotal']
    if 'SvscRevTotal' in doc:
        tstr['Services'] = doc['SvscRevTotal']
    if 'MaRevTotal' in doc:
        tstr['Annuity Services'] = doc['MaRevTotal']
    if 'ApplRevTotal' in doc:
        tstr['Appliances'] = doc['ApplRevTotal']
    if 'OthRevTotal' in doc:
        tstr['Other'] = doc['OthRevTotal']
    if 'IGFRevTotal' in doc:
        tstr['IGF'] = doc['IGFRevTotal']
    revenueTotals = json.dumps(tstr)
    # revenueTotals = revenueTotals.replace('"', "'")

    data = {
        'contractName': contractName,
        'fullContractName': '0' if not 'fullContractName' in doc else doc['fullContractName'],
        'contractNumber': '0' if not 'contractNumber' in doc else doc['contractNumber'],
        'matConValue': matConValue,
        'matConComments': '' if not 'MatConComments' in doc else removeNewLine(doc['MatConComments']),
        'contractStatus': 'Open',
        'contractStartDate': None if not 'contractStartDate' in doc else doc['contractStartDate'],
        'contractEndDate': None if not 'contractEndDate' in doc else doc['contractEndDate'],
        'OrigcontractEndDate': origcontractEndDate,
        'optContractExt': '' if not 'optContractExt' in doc else doc['optContractExt'],
        'optContractExtComments': '' if not 'optContractExtComments' in doc else removeNewLine(doc['optContractExtComments']),
        'multiYear': multiYear,
        'masterContentMgrID': None if not 'masterContentMgrID' in doc else doc['masterContentMgrID'],
        'masConCustNo': None if not 'masConCustNo' in doc else doc['masConCustNo'],
        'spaceDelReq': spaceDelReq,
        'spaceDelReqComments': None if not 'spaceDelReqComments' in doc else removeNewLine(doc['spaceDelReqComments']),
        'invReq': invReq,
        'invReqComments': invReqComments,
        'origFiscalYearPerD': None if not 'origFiscalYearPer' in doc else doc['origFiscalYearPer'],
        'contractType': contractType,
        secContractTypeKey: secContractTypeValue,
        'contractTerms': contractTerms,
        'pricingType': None if not 'pricingType' in doc else doc['pricingType'],
        'MasConComponType': comp_type_arr,
        'masContHWBrand': comp_type_hw_brand_arr,
        'masContESWsub': masContESWsub,
        'masContESWLic': masContESWLic,
        'masContESWcomments': None if not 'masContESWcomments' in doc else removeNewLine(doc['masContESWcomments']),
        'masContDSWsub': masContDSWsub,
        'CapOnDemand': capOnDemand,
        'CapOnDemandOpt': capOnDemandOpt,
        'CapOnDemandOptExp': None if not 'CapOnDemandOptExp' in doc else removeNewLine(doc['CapOnDemandOptExp']),

        'riskOfLoss': riskOfLoss,
        'riskOfLossReason': riskOfLossReason,
        'riskOfLossComments': None if not 'riskOfLossComments' in doc else removeNewLine(doc['riskOfLossComments']),
        'titlePasesToFedGov': titlePasesToFedGov,
        titlePasesToFedGovReasonKey: titlePasesToFedGovReasonValue,
        'titlePasesToFedGovComments': None if not 'titlePasesToFedGovComments' in doc else removeNewLine(doc['titlePasesToFedGovComments']),
        'futureConting': futureConting,
        'futureContingComments': None if not 'futureContingComments' in doc else removeNewLine(doc['futureContingComments']),
        'paymentBillp': paymentBillp,
        'paymentBillpComments': None if not 'paymentBillpComments' in doc else doc['paymentBillpComments'],
        'manualInvoiceingComments': None if not 'manualInvoiceingComments' in doc else removeNewLine(doc['manualInvoiceingComments']),
        'multiElementArrangement': multiElementArrangement,
        'multiElementArrangementDate': None if not 'multiElementArrangementDate' in doc else doc['multiElementArrangementDate'],
        'multiElementArrangementAcctNo': None if not 'multiElementArrangementAcctNo' in doc else doc['multiElementArrangementAcctNo'],
        'multiElementArrangementCommet': None if not 'multiElementArrangementCommet' in doc else removeNewLine(doc['multiElementArrangementCommet']),
        'classifiedAccount': '.' if not 'classifiedAccount' in doc else doc['classifiedAccount'],
        'otherTermCondition': otherTermCondition,
        'otherTermConditionComments': None if not 'otherTermConditionComments' in doc else removeNewLine(doc['otherTermConditionComments']),
        'contractProv': contractProv,
        'contractProvComments': None if not 'contractProvComments' in doc else removeNewLine(doc['contractProvComments']),
        'IFFApplicable': None if not 'IFFApplicable' in doc else doc['IFFApplicable'],

        'fsiName': '' if not 'fsiName' in doc else doc['fsiName'],
        'contractorType': contractor_type,
        'fsiCustNo': None if not 'fsiCustNo' in doc else doc['fsiCustNo'],
        'fsiAddress1': None if not 'fsiAddress1' in doc else doc['fsiAddress1'],
        'fsiAddress2': None if not 'fsiAddress2' in doc else doc['fsiAddress2'],
        'fsiCity': None if not 'fsiCity' in doc else doc['fsiCity'],
        'fsiState': fsi_state,
        'fsiZip': None if not 'fsiZip' in doc else doc['fsiZip'],
        'fsiContactName': None if not 'fsiContactName' in doc else doc['fsiContactName'],
        'fsiTitle': None if not 'fsiTitle' in doc else doc['fsiTitle'],
        'fsiPhone': None if not 'fsiPhone' in doc else doc['fsiPhone'],
        'fsiEmail': None if not 'fsiEmail' in doc else doc['fsiEmail'],
        'fsiComments': None if not 'fsiComments' in doc else removeNewLine(doc['fsiComments']),

        'custName': None if not 'custName' in doc else doc['custName'],
        'custNo': None if not 'custNo' in doc else doc['custNo'],
        'contactCompany': None if not 'contactCompany' in doc else doc['contactCompany'],
        'contactAddress1': None if not 'contactAddress1' in doc else doc['contactAddress1'],
        'contactAddress2': None if not 'contactAddress2' in doc else doc['contactAddress2'],
        'contactCity': None if not 'contactCity' in doc else doc['contactCity'],
        'contactState': contact_state,
        'contactZip': None if not 'contactZip' in doc else doc['contactZip'],
        'contactName': None if not 'contactName' in doc else doc['contactName'],
        'contactTitle': None if not 'contactTitle' in doc else doc['contactTitle'],
        'contactEmail': None if not 'contactEmail' in doc else doc['contactEmail'],
        'contactPhone': None if not 'contactPhone' in doc else doc['contactPhone'],
        'custComments': None if not 'contactComments' in doc else removeNewLine(doc['contactComments']),

        'creditApprovalStatus': creditApprovalStatus,
        'creditApprovalExpireDate': None if not 'creditApprovalExpireDate' in doc else doc['creditApprovalExpireDate'],
        'creditApprovalDate': None if not 'creditApprovalDate' in doc else doc['creditApprovalDate'],
        'escrowAgreementReceived': escrowAgreementReceived,
        'escrowCOD': escrowCOD,
        'escrowAgreeReceivedDate': None if not 'escrowAgreeReceivedDate' in doc else doc['escrowAgreeReceivedDate'],

        'custAddress1': '0' if not 'contactAddress1' in doc else doc['contactAddress1'],
        'custAddress2': '0' if not 'contactAddress2' in doc else doc['contactAddress2'],
        'custCity': '0' if not 'contactCity' in doc else doc['contactCity'],
        'custState': '0' if not 'contactState' in doc else doc['contactState'],
        'custZip': '0' if not 'contactZip' in doc else doc['contactZip'],
        'custContactName': '0' if not 'contactName' in doc else doc['contactName'],
        'custEmail': 'no_email@email.com' if not 'contactEmail' in doc else doc['contactEmail'],

        'contractMgr': {
            'email': '' if not 'ctlName' in doc else doc['ctlName'],
            'notesId': '' if not 'ctlLNID' in doc else doc['ctlLNID'],
            'name': '' if not 'ctlName' in doc else doc['ctlName'],
            'serial': '',
            'phone': '' if not 'ctlTl' in doc else doc['ctlTl'],
            'location': ''
        },
        'contractOwner': {
            'email': '' if not 'coName' in doc else doc['coName'],
            'notesId': '' if not 'coLNID' in doc else doc['coLNID'],
            'name': '' if not 'coName' in doc else doc['coName'],
            'serial': '',
            'phone': '' if not 'coTl' in doc else doc['coTl'],
            'location': ''
        },
        'ooId': {
            'email': '' if not 'ooName' in doc else doc['ooName'],
            'notesId': '' if not 'ooLNID' in doc else doc['ooLNID'],
            'name': '' if not 'ooName' in doc else doc['ooName'],
            'serial': '',
            'phone': '' if not 'ooTelephone' in doc else doc['ooTelephone'],
            'location': ''
        },
        'Div16_PMLNID': {
            'email': '' if not 'Div16_PMName' in doc else doc['Div16_PMName'],
            'notesId': '' if not 'Div16_PMLNID' in doc else doc['Div16_PMLNID'],
            'name': '' if not 'Div16_PMName' in doc else doc['Div16_PMName'],
            'serial': '',
            'phone': '' if not 'Div16_PMTelephone' in doc else doc['Div16_PMTelephone'],
            'location': ''
        },
        'Div16_PMOLNID': {
            'email': '' if not 'PMName' in doc else doc['PMName'],
            'notesId': '' if not 'PMLNID' in doc else doc['PMLNID'],
            'name': '' if not 'PMName' in doc else doc['PMName'],
            'serial': '',
            'phone': '' if not 'PMTelephone' in doc else doc['PMTelephone'],
            'location': ''
        },

        'reconCycleD': reconCycle,
        reconScheduleKey: reconScheduleValue,
        'offeringGrid': offeringGrid,  # '[{}]'
        'manualBillingGrid': manualBillingGrid,
        'revenueTotals': revenueTotals  # '{}'
    }

    if len(entries_to_delete) > 0:
        for entry in entries_to_delete:
            data = removeDictKey(data, entry)

    return data
