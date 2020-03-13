import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from netbuddyapp.models import RouterConfiguration
from ..connection import Connection


def get_router_config(router_config_id):
    # with sqlite3.connect(Connection.db_path) as conn:
    #     conn.row_factory = model_factory(Book)
    #     db_cursor = conn.cursor()

    #     db_cursor.execute("""
    #     SELECT
    #         b.id,
    #         b.title,
    #         b.isbn,
    #         b.author,
    #         b.year,
    #         b.librarian_id,
    #         b.location_id
    #     FROM libraryapp_book b
    #     WHERE b.id = ?
    #     """, (book_id,))

    #     return db_cursor.fetchone()
      
    return RouterConfiguration.objects.get(pk=router_config_id)


@login_required
def router_config_details(request, router_config_id):
    if request.method == 'GET':
        router_config = get_router_config(router_config_id)
        template_name = 'router/router_config_details.html'
        return render(request, template_name, {'router_config':router_config})