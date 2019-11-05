import pytest

import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('name', [
  ('cron')
])
def test_packages_are_installed(host, name):
    package = host.package(name)
    assert package.is_installed


@pytest.mark.parametrize('job,user', [
  ('0 */6 * * * backup.sh', 'admin'),
  ('@hourly rm -rf /tmp', 'root'),
])
def test_crontab_jobs_exist(host, job, user):
    jobs = host.check_output('crontab -u ' + user + ' -l')
    assert job in jobs


@pytest.mark.parametrize('file,job,user', [
  ('rsync', 'root * * * * * rsync -a /mnt /backup', 'root')
])
def test_cron_file_jobs_exist(host, file, job, user):
    cron_file = host.file('/etc/cron.d/' + file)
    assert cron_file.exists
    assert cron_file.is_file
    assert cron_file.user == user
    assert cron_file.group in [user, 'users']
    assert cron_file.contains(job)
