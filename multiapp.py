"""Frameworks for running multiple Streamlit applications as a single app.
"""
import streamlit as st

class MultiApp:
    """Framework for combining multiple streamlit applications.
    Usage:
        def foo():
            st.title("Hello Foo")
        def bar():
            st.title("Hello Bar")
        app = MultiApp()
        app.add_app("Foo", foo)
        app.add_app("Bar", bar)
        app.run()
    It is also possible keep each application in a separate file.
        import foo
        import bar
        app = MultiApp()
        app.add_app("Foo", foo.app)
        app.add_app("Bar", bar.app)
        app.run()
    """
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new application.
        Parameters
        ----------
        func:
            the python function to render this app.
        title:
            title of the app. Appears in the dropdown in the sidebar.
        """
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
        #     st.info(
        #     "🎈 **NEW:** 这里是测试)"
        # )
            # github-icon
            st.write(
            '''[![Star](https://img.shields.io/github/stars/NEDONION/lendingclub-webapp.svg?logo=github&style=social)](https://github.com/NEDONION/lendingclub-webapp)
                [![MAIL Badge](https://img.shields.io/badge/-nedjiachenghu@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:nedjiachenghu@gmail.com)](mailto:nedjiachenghu@gmail.com)
            ''')
        st.sidebar.title('Navigation')
        
        app = st.sidebar.radio(
            'Go to',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()
        
        st.sidebar.title('About')
        st.sidebar.info(
            """
            Applied Machine Learning Team 3 @ Tulane University
            - Yuchuan Han
            - Jiaquan Zhang
            - Yifan Xue
            - Kechun Yang
            - Jiacheng Hu
            
            """
                )