#include <Python/Python.h>
#include <iostream>

int main() {
	Py_Initialize();
	PyRun_SimpleString("from budget import Budget");
	PyRun_SimpleString("budget = Budget()");
	std::cout << PyRun_SimpleString("print(budget.bulk_load('json/receipt.json'))");
	Py_Finalize();
}
