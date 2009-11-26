#include "Python.h"
#include "pythonrun.h"
#include "import.h"

static PyObject*
init(PyObject *self, PyObject *args){
	Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
on_get_iter(PyObject *self, PyObject *args)
{
	static PyObject *rowref;
	static PyObject *result;
	static PyObject *selfobj;
	static PyObject *data;
	int index;
    if (!PyArg_ParseTuple(args, "OO", &selfobj, &rowref))
        return NULL;
    data = PyObject_GetAttrString(selfobj, "data");
    if (!data){
    	Py_DECREF(rowref);
		Py_DECREF(data);
    	Py_INCREF(Py_None);
    	return Py_None;
    }
    PyArg_ParseTuple(rowref, "i", &index);
    if (index <= PyList_Size(data) -1){
    	result = PyList_GetItem(data, index);
    }
    else{
    	Py_DECREF(rowref);
		Py_DECREF(data);
    	Py_INCREF(Py_None);
    	return Py_None;
    }
	if (!result){
		Py_DECREF(rowref);
		Py_DECREF(data);
		Py_INCREF(Py_None);
		return Py_None;
	}
	Py_XDECREF(rowref);
	Py_XDECREF(data);
    return Py_BuildValue("O", result);
}


static PyMethodDef CLibraryModelMethods[] = {
	{"__init__", init, METH_VARARGS, "doc string"},
    {"on_get_iter",  on_get_iter, METH_VARARGS,"Returns a ref."},
    {NULL, NULL}
};


static PyMethodDef ModuleMethods[] = { {NULL} };

#ifdef __cplusplus
extern "C"
#endif
PyMODINIT_FUNC
initCLibraryModel(void)
{

	PyMethodDef *def;

	PyObject *module = NULL;
	PyObject *moduleDict = NULL;
	PyObject *classDict = NULL;
	PyObject *className = NULL;
	PyObject *fooClass = NULL;

    module = Py_InitModule("CLibraryModel", ModuleMethods);
    moduleDict = PyModule_GetDict(module);
    classDict = PyDict_New();
    className = PyString_FromString("CLibraryModel");
    fooClass = PyClass_New(NULL, classDict, className);

	PyImport_AddModule("CLibraryModel");

    PyDict_SetItemString(moduleDict, "CLibraryModel", fooClass);
    Py_DECREF(classDict);
    Py_DECREF(className);
    Py_DECREF(fooClass);

    /* add methods to class */
    for (def = CLibraryModelMethods; def->ml_name != NULL; def++) {
    	PyObject *func = PyCFunction_New(def, NULL);
    	PyObject *method = PyMethod_New(func, NULL, fooClass);
    	PyDict_SetItemString(classDict, def->ml_name, method);
    	Py_DECREF(func);
    	Py_DECREF(method);
     }

}

int
main(int argc, char *argv[])
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initCLibraryModel();
    return 0;
}

