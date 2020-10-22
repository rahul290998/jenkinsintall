#!/usr/bin/env python3
def github_repo_present(data):
	has_changed = False
	meta = {"present": "not yet implemented"}
	return (has_changed, meta)

def github_repo_absent(data=None):
	has_changed = False
	meta = {"absent": "not yet implemented"}

def main():
    fields = {
		"github_auth_key": {"required": True, "type": "str"},
		"name": {"required": True, "type": "str" },
        "description": {"required": False, "type": "str"},
        "private": {"default": False, "type": "bool" },
        "has_issues": {"default": True, "type": "bool" },
        "has_wiki": {"default": True, "type": "bool" },
        "has_downloads": {"default": True, "type": "bool" },
        "state": {
        	"default": "present", 
        	"choices": ['present', 'absent'],  
        	"type": 'str' 
        },
	}
    choice_map = {
      "present": github_repo_present,
      "absent": github_repo_absent, 
    }
    module = AnsibleModule(argument_spec=fields)
    has_changed, result = choice_map.get(module.params['state'])(module.params)
    module.exit_json(changed=has_changed, meta=result)

def github_repo_present(data):

    api_key = data['github_auth_key']

    del data['state']
    del data['github_auth_key']

    headers = {
        "Authorization": "token {}" . format(api_key)
    }
    url = "{}{}" . format(api_url, '/user/repos')
    result = requests.post(url, json.dumps(data), headers=headers)

    if result.status_code == 201:
        return False, True, result.json()
    if result.status_code == 422:
        return False, False, result.json()

    # default: something went wrong
    meta = {"status": result.status_code, 'response': result.json()}
    return True, False, meta


def github_repo_absent(data=None):
    headers = {
        "Authorization": "token {}" . format(data['github_auth_key'])
    }
    url = "{}/repos/{}/{}" . format(api_url, "toast38coza", data['name'])
    result = requests.delete(url, headers=headers)

    if result.status_code == 204:
        return False, True, {"status": "SUCCESS"}
    if result.status_code == 404:
    	result = {"status": result.status_code, "data": result.json()}
    else:
        result = {"status": result.status_code, "data": result.json()}

