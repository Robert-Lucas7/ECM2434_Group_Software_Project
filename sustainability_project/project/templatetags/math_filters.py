from django import template

register = template.Library()

# Find the position of an item in the 'village grid' based on its row and column.
@register.filter
def find_grid_position(i,j):
    return i * 6 + j
