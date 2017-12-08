## Structure
```bash
└── ec2
    ├── ec2_ami_all_backup.py
    ├── ec2_ami_per_backup.py
    └── ec2_list_all_instances.py
```
## Execution
* Backup AMI of all instances from all regions
    * Instance tag has to have
```json
{"Key": "Auto_Backup"}
{"Name": "Yes"}
```
```bash
# -- How to run
python c2_ami_all_backup.py
```
