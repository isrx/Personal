import requests
import json
import sys

import dictobj

print('--> started')

counter = 50

origin_base_url = "http://9.57.199.231:8084/c_dir/FedContractMgmt.nsf"
origin_view_url = origin_base_url + \
    "/api/data/collections/name/MigrationUNIDs" + \
    "?start=" + str(counter) + "&count=50"

raw = requests.get(origin_view_url, verify=False)
entries = raw.json()


def lookupDoc(docUnid):
    doc_url = f"{origin_base_url}/api/data/documents/unid/{docUnid}"
    raw_doc = requests.get(doc_url, verify=False)
    return raw_doc.json()


# target_base_url = "https://transition-to-cloud.dal1a.ciocloud.nonprod.intranet.ibm.com/fcm-services/contract"  # UAT
target_base_url = "https://transition-to-cloud.dal1a.cirrus.ibm.com/fcm-services/contract"  # Prod
# target_headers = {"api-key": "pA17nSu90bRn3puKn5HoZjaTBLO25ULw"}
target_headers = {"Cookie": "dtLatC=1778; dtCookie=v_4_srv_6_sn_29187FB95B3706E12026353BDB8A6B61_perc_100000_ol_0_mul_1_app-3Aa7be052822a128bf_1_rcs-3Acss_0; rxVisitor=16204123661057IP0CBAOLEEBBQJAB80I1H7ID6KC27G9; dtPC=6$412366102_434h-vRHFKMSCRVFFHNSQMOKRTPKLUORCJAACM-0e11; rxvt=1620414520596|1620412366108; access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzX2hhc2giOiJPanZlWTJSbEhIOUtGelRDRDlHNDRBIiwidW5pcXVlU2VjdXJpdHlOYW1lIjoiMDc4NjA2NzgxIiwic3ViIjoiYWxmcmVkby5ndWlsbGVuMUBpYm0uY29tIiwiZG4iOiJ1aWQ9MDc4NjA2NzgxLGM9bXgsb3U9Ymx1ZXBhZ2VzLG89aWJtLmNvbSIsInJlYWxtTmFtZSI6IlczSURSZWFsbSIsIm5hbWUiOiJBTEZSRURPIERFIEpFU1VTIEdVSUxMRU4gT1JUSVoiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhbGZyZWRvLmd1aWxsZW4xQGlibS5jb20iLCJmaXJzdE5hbWUiOiJBTEZSRURPJTIwREUlMjBKRVNVUyIsImFjciI6InVybjppYm06c2VjdXJpdHk6cG9saWN5OmlkOjEzMTM3IiwidXNlclR5cGUiOiJmZWRlcmF0ZWQiLCJkaXNwbGF5TmFtZSI6IkFMRlJFRE8gREUgSkVTVVMgR1VJTExFTiBPUlRJWiIsImNuIjoiQUxGUkVETyUyMERFJTIwSkVTVVMlMjBHVUlMTEVOJTIwT1JUSVoiLCJqdGkiOiJ1TlQyY1R1OGhJTEZCTkZSeEEzM0c5WU50a25hRUsiLCJhdF9oYXNoIjoiN2xuWVp2bDFuODNEWFRSc2txTVFQZyIsImVtYWlsQWRkcmVzcyI6ImFsZnJlZG8uZ3VpbGxlbjFAaWJtLmNvbSIsImxhc3ROYW1lIjoiR1VJTExFTiUyME9SVElaIiwidWlkIjoiMDc4NjA2NzgxIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi53My5pYm0uY29tL29pZGMvZW5kcG9pbnQvZGVmYXVsdCIsImF1ZCI6Ik5UQTBOamcxTURFdE1qQmlNeTAwIiwiaWF0IjoxNjIwNDEyNDM0LCJleHAiOjE2MjA0MTk2MzR9.y2grkmxA8zKly0rmN4bcW2Oh1zviDqXWQHxbTH5tiaI; b16b28dc1c1189f6f100e31d6af4b939=2b36b944628c152356e5b17b3d5ffb4d; dtSa=-; ___tk67142224=1620412361540; CISESSIONIDPR02A=PBC5YS:2452117324; _hjid=19b7a88c-fb4e-428c-8236-8dbb6718298b; _abck=DCF69541EB3F3CC607DC3271370FF307~0~YAAQ5gB8aDZLbQx5AQAAQxs2OQW8a+elrT3mWYycVbekv5J8smzMQ6MKb8joVl6PaQbL7xayHd37UVfICHJe2gMrXOUme4yW/2QMi06RmJGFQ476/kDaKrAzdJvzZklx6FV3bARbGPKSFKlZ80o3+516li8FSh7Y59HjghoGYy+kcjem36JTYc0HN1XNAhhpvLzxFNyRRUmNDlbKxgLa4skLVq9pvwRWLvUC5VM8UfXnTmr43bWiUF0jHh4j5LyxHEWY7R0IlmJ0sfFjfkak1TPjToChmES9PlRdnzLDEmkR3beylWZs91qXQO14gWe9jdbAM0v/Gx+xSzHbbgPfiFb8Zz7W869F7+yj22fbaS0CAAkXHvsvg9z6FE4=~-1~-1~-1; optimizelyEndUserId=oeu1619025085597r0.8789195805624422; ajs_anonymous_id=%22538cce29-7f0c-4ab4-9948-dc131aa7feee%22; cd_user_id=179380972e7307-0ec022c01ac33d8-3e62694b-1fa400-179380972e8109d; AMCV_D10F27705ED7F5130A495C99%40AdobeOrg=359503849%7CMCMID%7C83912727734543657101305582337715398602%7CMCAAMLH-1620747611%7C9%7CMCAAMB-1620747611%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCCIDH%7C878910999%7CMCOPTOUT-1620150011s%7CNONE%7CMCSYNCSOP%7C411-18759%7CvVersion%7C5.0.1; utag_main=v_id:0179380965d80095d9b3247c0d9001075004d06d00bd0$_sn:1$_se:4$_ss:0$_st:1620144612505$ses_id:1620142810584%3Bexp-session$_pn:1%3Bexp-session$is_country_requiring_explicit_consent:false$dc_visit:1$dc_event:2%3Bexp-session$mm_sync:1%3Bexp-session$mm_ga_sync:1%3Bexp-session$dc_region:us-east-1%3Bexp-session; CoreM_State=15~-1~-1~-1~-1~3~3~5~3~3~7~7~|~~|~~|~~|~||||||~|~~|~~|~~|~~|~~|~~|~~|~; CoreM_State_Content=6~|~~|~|; _ga=GA1.2.1089872454.1620142812; ajs_user_id=%22IBMid-5500035XXN%22; OPTOUTMULTI=0:0%7Cc1:1%7Cc2:0%7Cc3:0; BMAID=538cce29-7f0c-4ab4-9948-dc131aa7feee; userContext=1|mx|0; CoreID6=50086736395715773744132&ci=50200000|BLUEMIX_50200000|Cloud_52640000|Cloud_51040000|IBMTESTW3_51040000|OneSrchProduction_51040000|HR_51040000|ARCHITECTURE_50200000|IBM_EVENTS_52640000|IBM_EVENTS_50200000|IBM_GlobalMarketing_52640000|IBM_GlobalMarketing_50200000|DWNEXT_50200000|Bluemix_50200000|IBMTESTWWW_51040000|NEWBLUEPAGES_50200000|IBM_WatsonHealth_52640000|IBM_WatsonHealth_50200000|www_50200000|ESTKCS_50200000|ESTDBL_50200000|MYIBM_52640000|DWNEXT_52640000|Bluemix_50200000|BLUEMIXTEST_50200000|CISO-Onboarding_51040000|HAIPRD_50200000|TRAINING_50200000|IBMSEC_51040000|METHODWEB_51040000|PP_50200000|IBM_GTS_50200000|ECOM_50200000|IBM_ConsolidatedAdvertising; experimentation_subject_id=ImQxNjhjNzhmLTE5YzgtNDA3MC04NzZhLTM2ZmI5ZDhmNDllYyI%3D--07cf65fb429e48185a45220604ad3b0fe187f728; UnicaNIODID=4GKvZQ5TSPY-bZFVPhR"}

for entry in entries:
    doc = lookupDoc(entry["@unid"])
    # doc = lookupDoc("3E707EA0827339D485258005007AB9B0")
    # print(f'--> unid({counter}): {doc["@unid"]}')

    data = dictobj.getDict(doc)

    # print(f'--> manualBillingGrid: {data["manualBillingGrid"]}')
    #print(f'--> data: {json.dumps(data)}')

    try:
        r = requests.post(
            target_base_url, headers=target_headers, json=data, verify=None)
        print(r)
        result = json.loads(r.text)
        if "id" in result:
            print(
                f'--> unid({counter}) {doc["@unid"]} uploaded with id {result["id"]}')
        elif "statusCode" in result and result["statusCode"] == 500:
            print(
                f'--> unid({counter}) {doc["@unid"]} failed to upload {r.text}')
        else:
            print(f'--> unid({counter}) {doc["@unid"]} unknown {r.text}')
    except:
        print(f'--> unid({counter}) unexpected error')
        print(sys.exc_info()[0])
        raise

    counter += 1
