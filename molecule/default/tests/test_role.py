import pytest


@pytest.mark.parametrize(
    "name",
    [
        ("cron"),
    ],
)
def test_packages_are_installed(host, name):
    package = host.package(name)
    assert package.is_installed


@pytest.mark.parametrize(
    "job,user",
    [
        ("0 */6 * * * backup.sh", "admin"),
        ("@hourly rm -rf /tmp", "root"),
    ],
)
def test_crontab_jobs_exist(host, job, user):
    jobs = host.check_output("crontab -u " + user + " -l")
    assert job in jobs


@pytest.mark.parametrize(
    "file,job",
    [
        ("rsync", "* * * * * root rsync -a /mnt /backup"),
        ("backup_database", "@daily admin /home/admin/mysqldump.sh"),
    ],
)
def test_cron_files_exist(host, file, job):
    cron_file = host.file("/etc/cron.d/" + file)
    assert cron_file.exists
    assert cron_file.is_file
    assert cron_file.user == "root"
    assert cron_file.group == "root"
    assert cron_file.contains(job)
