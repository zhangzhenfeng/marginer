# -*- coding: utf-8 -*-

from recognition.recorder import recorder

from recognition.translator import translator

filename = recorder.record_wave() 
translator.use_cloud(filename)