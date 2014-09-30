#include <Python.h>


static PyObject* spin(PyObject *self, PyObject *args) {
    return NULL;
}


static PyMethodDef module_methods[] = {
    {"spin", spin, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC init_find_golden_eggs(void) {
    PyObject *pymod = Py_InitModule("backend.games._find_golden_eggs", module_methods);
    if (pymod == NULL)
        return;
}
