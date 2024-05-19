# test_example.py
import pytest,re,os

def test_findpath():
    str1='200 I: AUTOMATION_REPORT Complete "NPI_TC-01_240509_100222923" "C:\\Users\\rante\\Documents\\VIAVI\\TM500\\5G NR\\Test Mobile Application\\Logged Data\\240509_100153_session" PASS'
    finalpath_match = re.search(r'C:\\.*_session', str1)
    finalpath = finalpath_match.group()
    last_part = os.path.basename(finalpath)
    print(last_part.split('\\')[-1])
    assert last_part is not None

if __name__ == "__main__":
    test_findpath()