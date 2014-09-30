#include <Python.h>

/**
 * =============================================================================
 * HELPERS
 * =============================================================================
 */



/**
 * =============================================================================
 * SPIN
 * =============================================================================
 *
 *     arguments: 
 *     ~~~~~~~~~~
 *         (dict)  session => User Session
 *         (int)   mid => Machine ID
 *         (float) bet => Bet
 *         (int)   lines => Bet Lines
 *
 *     return (tuple):
 *     ~~~~~~~~~~~~~~~
 *          (float) balance => New Balance (+/-) 
 *          (float) bet => New Bet (-) 
 *          (int)   lines => New Bet Lines (-) 
 *
 * =============================================================================
 */

static PyObject * spin(PyObject *self, PyObject *args, PyObject *keywds) {

    /* Arguments */
    
    PyObject *session;
    const int *mid;
    int *lines;
    float *bet;
    
    static char *kwlist[] = {
        "session", 
        "mid", 
        "bet", 
        "lines", 
        NULL
    };

    if (!PyArg_ParseTupleAndKeywords(
            args, keywds, "Oifi", kwlist, &session, &mid, &bet, &lines))
        return NULL;

    /* Validator */

    return Py_BuildValue("(i,f,i)", 200, .25, 30);
}


static PyMethodDef module_methods[] = {
    {"spin", (PyCFunction)spin, METH_VARARGS|METH_KEYWORDS, ""},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC init_slots(void) {
    PyObject *pymod = Py_InitModule("backend.games._slots", module_methods);
    if (pymod == NULL)
        return;
}
