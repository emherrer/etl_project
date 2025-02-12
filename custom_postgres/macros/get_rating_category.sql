{% macro get_rating_category(column_name) %}
    CASE
        WHEN {{ column_name }} >= 4.7 THEN 'Outstanding'
        WHEN {{ column_name }} >= 4.5 THEN 'Excellent'
        WHEN {{ column_name }} >= 4.3 THEN 'Good'
        WHEN {{ column_name }} >= 4.0 THEN 'Average'
        ELSE 'Poor'
    END
{% endmacro %}

