FROM curisca/millionaire_end



ADD requirements.txt /

RUN pip install -r /requirements.txt
ADD millionaire /millionaire/millionaire
ENV PYTHONPATH='/millionaire'
CMD ["python" , "millionaire/millionaire/agent/end_line.py"]