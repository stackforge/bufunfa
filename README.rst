Bufunfa

'Bufunfa' Brazilian / Portugese short for 'Money' is a ChargeBack / Billing
software in OpenStack / Cloud style.

Overview:
    Central:
        The main component that's interacted with using MQ RPC -
        typically Rabbit
    Recorder:
        The recorder typically fetches data from a external source like
        Ceilometer and transforms it into something useful to the system.
        It calls a procedure via the MQ RPC to store a "Record" which is the
        thing described above.

        A Recorder houses multiple plugins loaded via 'stevedore'

    API:
        Standard WSGI web services REST API.


Docs: http://bufunfa.rtfd.org
