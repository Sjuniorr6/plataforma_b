from django import template

register = template.Library()

@register.filter
def remover_duplicados(eventos):
    vistos = set()
    unicos = []
    for evento in eventos:
        if evento.qr_value not in vistos:
            vistos.add(evento.qr_value)
            unicos.append(evento)
    return unicos
