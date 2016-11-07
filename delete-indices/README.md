
# Delete Indices based on status

Delete elasticsearch indices by status.

## Install python requirements

~~~bash
pip install -r requirements.txt
~~~

## Run

~~~
chmod u+x delete-indices.py
~~~

### Delete closed indices

~~~
./delete-indices.py elk-server:9200
~~~

### Delete open indices

~~~
./delete-indices.py elk-server:9200 -s open
~~~

### Dry-Run

~~~
./delete-indices.py elk-server:9200 --dry-run
~~~

## Lint python script

~~~
flake8 **/*.py
~~~

## Code Metrics

~~~
radon cc . -a -nc
~~~

## UnitTest

~~~
py.test --html=report.html
~~~

## Line Count

~~~
find . -name '*.py' | xargs wc -l
~~~

## License

MIT / BSD

## Author Information

John Paul Newman
