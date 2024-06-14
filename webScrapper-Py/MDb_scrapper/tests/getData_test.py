import os
import sys

import pytest # needs to install pytest-asyncio plugin for async tests

# importing from a parent directory
current_dir = os.path.dirname(os.path.abspath(__file__)) # Get the absolute path of the current file
main_dir = os.path.join(current_dir, '..') # Add the directory containing main.py to the Python path
sys.path.append(main_dir)

from getData import getActorData

test_data = [
    {
        'nameID': "nm0647634",
        'gender': "f",
        'result': {'first_name': 'Elizabeth', 'last_name': 'Olsen', 'birth_date': '1989-2-16', 'birth_place_state': ' California', 'birth_place_country': ' USA', 'mother_first_name': 'Jarnette', 'mother_last_name': 'Olsen', 'father_first_name': 'David', 'father_last_name': 'Olsen', 'gender': 'f', 'ethnicity': 'None'}
    },
    {
        'nameID': "nm3009232",
        'gender': "m",
        'result': {'first_name': 'Ezra', 'last_name': 'Miller', 'birth_date': '1992-9-30', 'birth_place_state': ' New Jersey', 'birth_place_country': ' USA', 'mother_first_name': 'Marta', 'mother_last_name': 'Koch', 'father_first_name': 'Robert', 'father_last_name': 'Miller', 'gender': 'm', 'ethnicity': 'None'}
    },
    { # not getting name for some reason
        'nameID': "nm0451307",
        'gender': "m",
        'result': {}
    }
    { # don't have satte data, only country
        'nameID': "nm0266622",
        'gender': "m",
        'result': {}
    }
]

@pytest.mark.asyncio
async def test_getActorData():
    for test in test_data:
        res = await getActorData(test['nameID'], test['gender'], isSave=False)
        assert(res == test['result'])
