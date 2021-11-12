FROM curisca/millionaire


ADD millionaire /millionaire
ENV PYTHONPATH='/millionaire'
ENTRYPOINT ["python"]
CMD ['/millionaire/aggent/base_line.py']