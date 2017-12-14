
#include <Python.h>
#include <stdio.h>

#include "libirig106/src/irig106ch10.h"


PyObject * _i106_open(PyObject *self, PyObject *args){
    const char *filename;
    int mode, handle;
    if (!PyArg_ParseTuple(args, "si", &filename, &mode))
        return NULL;

    I106Status status = I106C10Open(&handle, filename, (I106C10Mode)mode);
    return Py_BuildValue("ii", (int) status, handle);
}

PyObject * _i106_next_header(PyObject *self, PyObject *args){
    int handle;
    if (!PyArg_ParseTuple(args, "i", &handle))
        return NULL;

    I106C10Header header;
    I106Status status = I106C10ReadNextHeader(handle, &header);

    return Py_BuildValue("ii", (int)status, (int)&header);
}

static PyMethodDef funcs[] = {
    {"i106_open", _i106_open, METH_VARARGS, "Open a chapter 10 file"},
    {"i106_next_header", _i106_next_header, METH_VARARGS, "Read the next header from an open file"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef _i106 = {
    PyModuleDef_HEAD_INIT, "_i106", "docstring", -1, funcs
};

PyMODINIT_FUNC PyInit__i106(void){
    return PyModule_Create(&_i106);
}

int main(int argc, char *argv[]){
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */
    PyImport_AppendInittab("_i106", PyInit__i106);

    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(program);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
     *        import can be deferred until the embedded
     *        script
     *               imports it. */
    PyImport_ImportModule("spam");

    PyMem_RawFree(program);
    return 0;
}
