FROM curisca/millionaire


ADD requirements.txt /

RUN pip install -r /requirements.txt
ADD millionaire /millionaire/millionaire
ENV PYTHONPATH='/millionaire'
CMD ["python" , "millionaire/millionaire/agent/base_line.py"]