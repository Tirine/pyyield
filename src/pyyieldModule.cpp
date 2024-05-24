#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <thread>

// Only added for IDE complaint.
#ifndef NULL
#define NULL nullptr
#endif

static PyObject* pyyield(PyObject* self, PyObject* args) {
	// Just yield, nothing else.
	::std::this_thread::yield();
	Py_RETURN_NONE;
}

static PyMethodDef PyYieldMethods[] = {
	{"pyyield", pyyield, METH_NOARGS, "Execute a OS thread 'yield' command."},
	{nullptr, nullptr, 0, nullptr} /* Sentinel */
};

static struct PyModuleDef pyyieldmodule
	= {PyModuleDef_HEAD_INIT,
	   "pyyield", /* name of module */
	   nullptr,	  /* module documentation, may be NULL */
	   -1,		  /* size of per-interpreter state of the module,
					 or -1 if the module keeps state in global variables. */
	   PyYieldMethods};

PyMODINIT_FUNC PyInit_pyyield(void) { return PyModule_Create(&pyyieldmodule); }

int main(int argc, char* argv[]) {
	PyStatus status;
	PyConfig config;

	PyConfig_InitIsolatedConfig(&config);
	status = PyConfig_SetBytesArgv(&config, argc, argv);

	if (PyStatus_Exception(status)) {
		fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
		PyConfig_Clear(&config);
		Py_ExitStatusException(status);
	}

	status = Py_InitializeFromConfig(&config);
	if (PyStatus_Exception(status)) {
		fprintf(stderr, "Error: could not extend in-built modules table\n");
		PyConfig_Clear(&config);
		Py_ExitStatusException(status);
	}
	PyConfig_Clear(&config);

	/* Optionally import the module; alternatively,
	   import can be deferred until the embedded script
	   imports it. */
	PyObject* pmodule = PyImport_ImportModule("pyyield");
	if (!pmodule) {
		PyErr_Print();
		fprintf(stderr, "Error: could not import module 'pyyield'\n");
		PyConfig_Clear(&config);
		Py_ExitStatusException(status);
	}

	return 0;
}
