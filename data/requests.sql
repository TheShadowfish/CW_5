--Запросы, которые необходимо было реализовать

--Получает список всех компаний и количество вакансий у каждой компании. get_companies_and_vacancies_count
SELECT  * from employers JOIN
	(SELECT employer_id, COUNT(*) AS "vacancies" FROM vacancies JOIN employers USING(employer_id) GROUP BY employer_id) AS vacancy_counter
	USING (employer_id)  ORDER BY vacancy_counter.vacancies DESC;

--Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.get_companies_and_vacancies_count

SELECT vacancies.name AS vacancy, employers.name AS employer, salary, vacancies.url, region_name, requirements
	FROM vacancies
	JOIN regions USING (region_id)
	JOIN employers USING (employer_id)
	ORDER BY vacancies.salary DESC;

--Получает среднюю зарплату по вакансиям

SELECT vacancies.name, AVG(vacancies.salary), COUNT(vacancies.name) AS number_of_vacancies FROM vacancies GROUP BY vacancies.name
	ORDER BY AVG(vacancies.salary) DESC;

--Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям

SELECT * FROM vacancies,
	(SELECT AVG(vacancies.salary) AS middle_salary FROM vacancies WHERE vacancies.salary > 0) AS vacancy_avg
	WHERE vacancies.salary > vacancy_avg.middle_salary
	ORDER BY vacancies.salary DESC;

--Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python

SELECT * FROM vacancies
	WHERE vacancies.name LIKE '%python%'
	OR vacancies.name LIKE '%developer%'
	OR vacancies.name LIKE '%Python%'
	ORDER BY vacancies.name DESC;

SELECT * FROM vacancies
	WHERE vacancies.name LIKE '%Python%'
	ORDER BY vacancies.name DESC;