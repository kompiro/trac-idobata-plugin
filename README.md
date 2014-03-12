Trac Idobata Plugin
===================

Trac event hook for Idobata 

## How to install

1. Add hook to your room at idobata
1. Build this plugin 

        git clone https://github.com/kompiro/trac-idobata-plugin
        python setup.py bdist_egg
        cp dist/TracSevabotNotificationPlugin-VERSION-PYTHON_VERSION.egg YOUR_TRAC_ENV/plugins

1. Configure your trac env. Open your conf/trac.ini and set your env value like below.

        [idobata]
        endpoint = http://idobata.io/XXX # The room's hook endpoint

        # This plugin provides two notifications ticket, and wiki.
        [component]
        idobata.notification.TicketNotification = enabled
        idobata.notification.WikiNotification = enabled

1. Restart Trac

## License
Copyright 2014 Hiroki Kondo<kompiro@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
