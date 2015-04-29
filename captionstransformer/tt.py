from captionstransformer import core
from datetime import datetime, timedelta

class Reader(core.Reader):
    def text_to_captions(self):
        caption = core.Caption()
        lines = self.rawcontent.split('\n')
        lines_count = len(lines)
        for i in range(lines_count-1):
            start = lines[i][0:12]
            end = lines[i+1][0:12]
            text = lines[i][13:]
                       
            if start is not None:
                #means it is a new caption so start by close previous one
                if caption.text:
                    self.add_caption(caption)
                if end == "":
                    end = start
                caption = core.Caption()
                caption.start = datetime.strptime(start, '%H:%M:%S:%f')
                caption.end = datetime.strptime(end, '%H:%M:%S:%f')
                caption.text = text
        
        self.add_caption(caption)

        return self.captions

class Writer(core.Writer):
    DOCUMENT_TPL = u"%s"
    CAPTION_TPL = u"""%(start)s %(text)s\n"""

    def format_time(self, caption):
        """Return start and end time for the given format"""

        return {'start': caption.start.strftime('%H:%M:%S:%f')[:-3]}

    def get_template_info(self, caption):
        info = self.format_time(caption)
        info['text'] = caption.text.replace("\n", " ")
        return info