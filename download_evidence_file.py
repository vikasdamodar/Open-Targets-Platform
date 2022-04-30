import ftplib
import datetime
import multiprocessing
from io import BytesIO


class DownloadEvidence():
    ftp = ftplib.FTP('ftp.ebi.ac.uk')
    ftp.login()
    ftp.cwd('pub/databases/opentargets/platform/21.11/output/etl/json/evidence/sourceId=eva')

    def fetch_content(self, file):
        # Fetch the content and add to byte stream for parallel processing
        r = BytesIO()
        self.ftp.retrbinary("RETR " + file, r.write)
        return r.getvalue()

    def write_to_local_file(self):
        # Starting multi procesing for downloding multiple files at a time
        p = multiprocessing.Pool(30)
        files = self.ftp.nlst()
        with open("evidence.json", 'a+b') as f:
            for result in p.imap(self.fetch_content, files):
                f.write(result)

    def close_ftp(self):
        self.ftp.close()


if __name__ == '__main__':
    print("Downloading evidence.......")
    DownloadEvidence().write_to_local_file()
    DownloadEvidence().close_ftp()
