import adm.models as adm
from django.core.mail import send_mail
from django.template.loader import render_to_string

atos = {
    'adm': {
        '1': adm.OficioInternoAdm,
        '2': adm.OficioExternoAdm,
        '3': adm.DespachoAdm,
        '4': adm.StatusAdm,
        '5': adm.MidiaAdm,
        '6': adm.DocumentosGeraisAdm,
        '7': adm.ControlEmpresas,
    }
}


def send_to_email_users(context, test=False):
    unsent_notices = context['unsent_notices']
    unsent_emails = context['user_emails']
    context_email = {
        'msg': context['msg'],
        'email': ', '.join(unsent_emails),
    }
    html = render_to_string('componentes/shares/TemplateEmailNotficacao.html', context_email)

    send_mail(
        subject="[GEP] Você recebeu uma nova notificação",
        message=context_email['msg'],
        from_email='gep@noreply.ssp.pi.gov.br',
        recipient_list=unsent_emails,
        fail_silently=not test,
        html_message=html
    )

    for notice in unsent_notices:
        notice.emailed = True
        notice.save()
