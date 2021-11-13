FROM curisca/millionaire


ADD millionaire /millionaire/millionaire
ENV PYTHONPATH='/millionaire'
CMD ["python" , "millionaire/millionaire/agent/base_line.py"]