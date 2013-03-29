try:
    import resource
except ImportError:
    pass  # Will fail on Win32 systems
import time

from iktomi_toolbar.panels import DebugPanel


class Timer(DebugPanel):

    name = 'Timer'

    try:
        resource
    except NameError:
        has_content = False
        has_resource = False
    else:
        has_content = True
        has_resource = True

    def nav_subtitle(self):
        self.process_response(None)
        if self.has_resource:
            utime = self._end_rusage.ru_utime - self._start_rusage.ru_utime
            stime = self._end_rusage.ru_stime - self._start_rusage.ru_stime
            return 'CPU: %0.2fms (%0.2fms)' % ((utime + stime) * 1000.0,
                                               self.total_time)
        else:
            return 'TOTAL: %0.2fms' % self.total_time

    def content(self):
        utime = 1000 * self._elapsed_ru('ru_utime')
        stime = 1000 * self._elapsed_ru('ru_stime')
        vcsw = self._elapsed_ru('ru_nvcsw')
        ivcsw = self._elapsed_ru('ru_nivcsw')

        rows = (('User CPU time', '%0.3f msec' % utime),
                ('System CPU time', '%0.3f msec' % stime),
                ('Total CPU time', '%0.3f msec' % (utime + stime)),
                ('Elapsed time', '%0.3f msec' % self.total_time),
                ('Context switches', '%d voluntary, %d involuntary' % (vcsw,
                                                                       ivcsw)))
        context = self.context.copy()
        context.update({'rows': rows})

        return self.render('panels/timer.html', context)

    def process_request(self, request):
        self._start_time = time.time()
        if self.has_resource:
            self._start_rusage = resource.getrusage(resource.RUSAGE_SELF)

    def process_response(self, response):
        self.total_time = (time.time() - self._start_time) * 1000
        if self.has_resource:
            self._end_rusage = resource.getrusage(resource.RUSAGE_SELF)

    def _elapsed_ru(self, name):
        return (getattr(self._end_rusage, name) -
                getattr(self._start_rusage, name))
