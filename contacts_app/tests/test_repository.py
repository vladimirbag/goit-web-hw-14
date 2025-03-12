import unittest
from routes.contacts import YourClass 

class TestRepository(unittest.TestCase):  # успадковуємо від TestCase
    def test_example(self):
        repo = YourClass()  # створення екземпляра класу
        self.assertEqual(repo.some_method(), "Очікуваний результат")  # перевірка результату

if __name__ == '__main__':
    unittest.main()  # викликає виконання всіх тестів
