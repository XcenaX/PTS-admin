# projects/templatetags/admin_dashboard.py
from django import template
from django.urls import reverse
from django.templatetags.static import static

from projects.models import CompanyProject

register = template.Library()


@register.inclusion_tag("admin/_dashboard_content.html", takes_context=True)
def render_dashboard(context):
    request = context["request"]

    qs = CompanyProject.objects.all()

    # scoping: обычный админ видит только свою компанию
    if not request.user.is_superuser:
        # поменяй путь, если company лежит иначе
        qs = qs.filter(company=request.user.userprofile.company)

    total = qs.count()
    active = qs.filter(is_active=True).count()

    no_point = qs.filter(map_x__isnull=True).count() + qs.filter(map_y__isnull=True).count()
    # чтобы не считать дважды, если оба null:
    no_point = qs.filter(map_x__isnull=True, map_y__isnull=True).count()

    no_hero = qs.filter(hero_image__isnull=True).count()
    no_summary = qs.filter(summary__exact="").count()
    no_role = qs.filter(role_in_project__exact="").count()

    # ссылки в админку
    app_label = CompanyProject._meta.app_label
    model_name = CompanyProject._meta.model_name

    changelist_url = reverse(f"admin:{app_label}_{model_name}_changelist")
    add_url = reverse(f"admin:{app_label}_{model_name}_add")

    def cl(params: str) -> str:
        return f"{changelist_url}?{params}" if params else changelist_url

    # последние обновления
    latest = qs.order_by("-updated_at")[:10]

    # точки для мини-карты
    points_qs = qs.filter(is_active=True, map_x__isnull=False, map_y__isnull=False).only("id", "title", "map_x", "map_y")
    points = []
    for p in points_qs:
        x = float(p.map_x) * 100
        y = float(p.map_y) * 100
        change_url = reverse(f"admin:{app_label}_{model_name}_change", args=[p.id])
        points.append({
            "id": p.id,
            "title": p.title,
            "x_pct": format(x, ".6f"),
            "y_pct": format(y, ".6f"),
            "change_url": change_url,
        })

    # картинка карты (положи файл сюда: static/img/kz_map.png)
    map_image_url = static("img/kz_map.png")

    return {
        "total": total,
        "active": active,
        "no_point": no_point,
        "no_hero": no_hero,
        "no_summary": no_summary,
        "no_role": no_role,

        "changelist_url": changelist_url,
        "add_url": add_url,

        "link_no_point": cl("map_x__isnull=1&map_y__isnull=1"),
        "link_no_hero": cl("hero_image__isnull=1"),
        "link_no_summary": cl("summary__exact="),
        "link_no_role": cl("role_in_project__exact="),
        "link_active": cl("is_active__exact=1"),

        "latest": latest,
        "points": points,
        "map_image_url": map_image_url,
    }
