ansible-role-cron
=================

This role configures cron jobs.

Requirements
------------

Ansible 2.6 or newer.

Supported Platforms
-------------------

- [Debian - 9 (Stretch)](https://wiki.debian.org/DebianStretch)
- [Debian - 10 (Buster)](https://wiki.debian.org/DebianBuster)
- [Ubuntu - 18.04 (Bionic Beaver)](http://releases.ubuntu.com/18.04/)
- [Ubuntu - 20.04 (Focal Fossa)](http://releases.ubuntu.com/20.04/)

Role Variables
--------------

| Variable                     | Required | Default                         | Choices   | Comments                                      |
|------------------------------|----------|---------------------------------|-----------|-----------------------------------------------|
| cron_dependencies            | yes      | `[cron]`                        | list      |                                               |
| cron_jobs                    | yes      | `[]`                            | list      | Cron jobs to install. See `defaults/main.yml` |

Dependencies
------------

None

Example Playbook
----------------

    - hosts: all
      roles:
        - ansible-role-cron
          cron_jobs:
            - name: "run backup script every 6 hours as admin"
              job: backup.sh
              hour: "*/6"
              minute: 0
              user: admin
            - name: "delete files in /tmp every hour as root"
              job: "rm -rf /tmp"
              special_time: "hourly"
            - name: "rsync files between 2 directories every 15 minutes using /etc/cron.d/rsync as root"
              job: "rsync -a /mnt /backup"
              cron_file: "rsync"
              user: root
            - name: "backup database daily using /etc/cron.d/backup_database as admin"
              job: "/home/admin/mysqldump.sh"
              cron_file: "backup_database"
              special_time: "daily"
              user: admin

Testing
-------

    molecule test

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
