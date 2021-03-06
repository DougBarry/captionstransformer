from datetime import datetime, timedelta

class Reader(object):
    def __init__(self, fileobject):
        self.fileobject = fileobject
        self.captions = []
        self.rawcontent = None
        self.encoding = 'utf-8'

    def read(self):
        self.rawcontent = self.fileobject.read()
        if type(self.rawcontent) == str:
            try:
                self.rawcontent = self.rawcontent.decode(self.encoding)
            except (AttributeError, UnicodeDecodeError) as e:
                pass

        self.text_to_captions()
        return self.captions

    def add_caption(self, caption):
        self.captions.append(caption)

    def __repr__(self):
        return u"%s.%s: %s" % (self.__class__.__module__,
                               self.__class__.__name__,
                               "\n".join([caption.text\
                                          for caption in self.captions
                                          if hasattr(caption, 'text')]))

    def close(self):
        self.fileobject.close()

    def text_to_captions(self):
        """must be implemented in subclass"""
        pass

    def adapt_time_string(self, time_str):

        colons = time_str.count(':')
        dots = time_str.count('.')
        commas = time_str.count(',')

        if commas:
            try:
                return datetime.strptime(time_str, "%H:%M:%S,%f")
            except ValueError as v:
                raise v

        if dots:
            try:
                return datetime.strptime(time_str, "%H:%M:%S.%f")
            except ValueError as v:
                raise v

        if colons == 2:
            try:
                return datetime.strptime(time_str, '%H:%M:%S')
            except ValueError as v:
                raise v
        elif colons == 3:
            # bad format...
            try:
                return datetime.strptime(time_str, '%H:%M:%S:%f')
            except ValueError as v:
                raise v


class Writer(object):
    DOCUMENT_TPL = u"%s"
    CAPTION_TPL = u"%(start)s , %(end)s , %(text)s"

    def __init__(self, fobject, captions=None):
        self.fileobject = fobject
        self.captions = []
        self.encoding = 'utf-8'
        if captions is not None:
            self.captions = captions

    def add_caption(self, caption):
        self.captions.append(caption)

    def set_captions(self, captions):
        self.captions = captions

    def write(self, captions=None):
        if captions is not None:
            self.captions = captions
        value = self.captions_to_text()
        self.fileobject.write(value.encode(self.encoding))

    def close(self):
        self.fileobject.close()

    def captions_to_text(self):
        text = self.DOCUMENT_TPL
        buffer = u""
        for caption in self.captions:
            buffer += self.CAPTION_TPL % self.get_template_info(caption)
        return text % buffer

    def format_time(self, caption):
        return {'start': caption.start.strftime('%H:%M:%S'),
                'end': caption.end.strftime('%H:%M:%S')}

    def get_template_info(self, caption):
        info = self.format_time(caption)
        info['text'] = caption.text
        return info


class Caption(object):
    def __init__(self):
        self._duration = None
        self._start = None
        self._end = None
        self._text = u""
        self.encoding = "utf-8"

    def update(self):
        if self._end is None and\
           self._start is not None and\
           self._duration is not None:
            self._end = self.start + self.duration
        if self._duration is None and\
           self._start is not None and\
           self._end is not None:
            self._duration = self._end - self._start

    def get_duration(self):
        return self._duration

    def set_duration(self, value):
        if type(value) != timedelta:
            raise ValueError('duration must be a timedelta: %s' % value)
        self._duration = value
        self.update()

    duration = property(get_duration, set_duration)

    def get_start(self):
        return self._start

    def set_start(self, value):
        if type(value) != datetime:
            raise ValueError('start must be a datetime instance: %s' % type(value))
        self._start = value
        self.update()

    start = property(get_start, set_start)

    def get_end(self):
        return self._end

    def set_end(self, value):
        if type(value) != datetime:
            raise ValueError('start must be a datetime instance: %s' % type(value))
        self._end = value
        self.update()

    end = property(get_end, set_end)

    def get_text(self):
        return self._text

    def set_text(self, value):
        if type(value) == str:
            try:
                value = str.decode(self.encoding)
            except AttributeError:
                pass

        elif type(value) != unicode:
            raise ValueError("text must be either encoded string or unicode")
        self._text = value

    text = property(get_text, set_text)

    def __repr__(self):
        return u"%s.%s: %s" % (self.__class__.__module__,
                               self.__class__.__name__,
                               self.text)


    def get_date_from_delta(self, t_hour=0, t_minute=0, t_second=0, t_millisecond=0, t_microsecond=0):
        """return a reference date to 1901-01-01 to work with time"""
        dt = None
        if t_second > 59:
            dt = timedelta(seconds=t_second)
            t_second = 0
        if t_millisecond:
            t_microsecond += t_millisecond * 1000
        date = datetime(year=1900, month=1, day=1, hour=t_hour, minute=t_minute,
                        second=t_second, microsecond=t_microsecond)
        if dt:
            date += dt
        return date

