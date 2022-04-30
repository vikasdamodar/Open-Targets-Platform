import ftplib
import datetime
import multiprocessing
from io import BytesIO


class DownloadTargets():
    ftp = ftplib.FTP('ftp.ebi.ac.uk')
    ftp.login()
    ftp.cwd('pub/databases/opentargets/platform/21.11/output/etl/json/targets/')

    def fetch_content(self, file):
        print(file, datetime.datetime.now())
        r = BytesIO()
        self.ftp.retrbinary("RETR " + file, r.write)
        return r.getvalue()

    def write_to_local_file(self):
        p = multiprocessing.Pool(30)
        files = self.ftp.nlst()
        with open("targets.json", 'a+b') as f:
            for result in p.imap(self.fetch_content, files):
                f.write(result)

    def close_ftp(self):
        self.ftp.close()


if __name__ == '__main__':
    print("Downloading targets........")
    DownloadTargets().write_to_local_file()
    DownloadTargets().close_ftp()
