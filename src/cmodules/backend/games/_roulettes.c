#include <Python.h>


static PyObject* spin(PyObject *self, PyObject *args) {
    return NULL;
}


static PyMethodDef module_methods[] = {
    {"spin", spin, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC init_roulettes(void) {
    PyObject *pymod = Py_InitModule("backend.games._roulettes", module_methods);
    if (pymod == NULL)
        return;
}
