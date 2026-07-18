from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Count
from io import BytesIO
import os

from django.http import FileResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor

import qrcode

from datetime import date

from .models import Prisonnier



# ==========================
# TABLEAU DE BORD
# ==========================

@login_required(login_url='login')
def dashboard(request):

    total = Prisonnier.objects.count()

    encours = Prisonnier.objects.filter(
        statut="encours"
    ).count()

    liberes = Prisonnier.objects.filter(
        statut="libere"
    ).count()


    liste = Prisonnier.objects.filter(
        date_sortie=date.today()
    )


    aujourdhui = liste.count()


    retard = Prisonnier.objects.filter(
        date_sortie__lt=date.today(),
        statut="encours"
    ).count()


    context = {
        "total": total,
        "encours": encours,
        "liberes": liberes,
        "aujourdhui": aujourdhui,
        "retard": retard,
        "liste": liste,
    }


    return render(
        request,
        "prisonniers/dashboard.html",
        context
    )



# ==========================
# CARTE PRISONNIER
# ==========================

def carte_prisonnier(request, pk):

    prisonnier = get_object_or_404(
        Prisonnier,
        pk=pk
    )


    buffer = BytesIO()


    largeur = 85.6 * mm
    hauteur = 54 * mm


    pdf = canvas.Canvas(
        buffer,
        pagesize=(largeur, hauteur)
    )


    # ==========================
    # RECTO
    # ==========================


    pdf.setFillColor(
        HexColor("#0F4C81")
    )

    pdf.rect(
        0,
        0,
        largeur,
        hauteur,
        fill=1
    )


    # Motif sécurité

    pdf.setFillColor(
        HexColor("#246BA6")
    )

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        12*mm,
        20*mm,
        "CARCERALNET"
    )


    # Drapeau RDC

    drapeau = os.path.join(
        settings.BASE_DIR,
        "prisonniers",
        "static",
        "images",
        "drapeau_rdc.png"
    )


    if os.path.exists(drapeau):

        pdf.drawImage(
            ImageReader(drapeau),
            5*mm,
            45*mm,
            width=14*mm,
            height=7*mm
        )


    # Logo

    logo = os.path.join(
        settings.BASE_DIR,
        "prisonniers",
        "static",
        "images",
        "logo.png"
    )


    if os.path.exists(logo):

        pdf.drawImage(
            ImageReader(logo),
            67*mm,
            44*mm,
            width=13*mm,
            height=7*mm
        )


    pdf.setFillColorRGB(
        1,
        1,
        1
    )


    pdf.setFont(
        "Helvetica-Bold",
        8
    )


    pdf.drawString(
        25*mm,
        47*mm,
        "CARCERALNET"
    )



    # PHOTO

    if prisonnier.photo:

        chemin_photo = prisonnier.photo.path


        if os.path.exists(chemin_photo):

            pdf.drawImage(
                ImageReader(chemin_photo),
                5*mm,
                14*mm,
                width=22*mm,
                height=26*mm
            )



    # Informations simples

    pdf.setFont(
        "Helvetica",
        6.5
    )


    pdf.drawString(
        32*mm,
        37*mm,
        f"N° : {prisonnier.numero_prisonnier}"
    )


    pdf.drawString(
        32*mm,
        33*mm,
        f"Nom : {prisonnier.nom}"
    )


    pdf.drawString(
        32*mm,
        29*mm,
        f"Postnom : {prisonnier.postnom}"
    )


    pdf.drawString(
        32*mm,
        25*mm,
        f"Prenom : {prisonnier.prenom}"
    )


    pdf.drawString(
        32*mm,
        21*mm,
        f"Cellule : {prisonnier.cellule}"
    )



    # QR CODE

    qr = qrcode.make(
        f"CARCERALNET-{prisonnier.numero_prisonnier}"
    )


    qr_buffer = BytesIO()


    qr.save(
        qr_buffer,
        format="PNG"
    )


    qr_buffer.seek(0)


    pdf.drawImage(
        ImageReader(qr_buffer),
        69*mm,
        5*mm,
        width=11*mm,
        height=11*mm
    )



    # ==========================
    # VERSO
    # ==========================


    pdf.showPage()


    pdf.setFillColor(
        HexColor("#FFFFFF")
    )


    pdf.rect(
        0,
        0,
        largeur,
        hauteur,
        fill=1
    )


    # Bande supérieure

    pdf.setFillColor(
        HexColor("#0F4C81")
    )

    pdf.rect(
        0,
        47*mm,
        largeur,
        7*mm,
        fill=1
    )



    pdf.setFillColorRGB(
        1,
        1,
        1
    )


    pdf.setFont(
        "Helvetica-Bold",
        8
    )


    pdf.drawString(
        8*mm,
        49*mm,
        "CARCERALNET RDC"
    )



    # Informations verso

    pdf.setFillColorRGB(
        0,
        0,
        0
    )


    pdf.setFont(
        "Helvetica",
        7
    )


    pdf.drawString(
        8*mm,
        38*mm,
        f"Motif : {prisonnier.motif}"
    )


    pdf.drawString(
        8*mm,
        32*mm,
        f"Entrée : {prisonnier.date_entree}"
    )


    pdf.drawString(
        8*mm,
        26*mm,
        f"Nationalité : {prisonnier.nationalite}"
    )



    # Signature directeur

    signature = os.path.join(
        settings.BASE_DIR,
        "prisonniers",
        "static",
        "images",
        "signature.png"
    )


    if os.path.exists(signature):

        pdf.drawImage(
            ImageReader(signature),
            58*mm,
            8*mm,
            width=20*mm,
            height=10*mm
        )


    pdf.drawString(
        60*mm,
        5*mm,
        "Directeur"
    )



    pdf.save()


    buffer.seek(0)


    return FileResponse(
        buffer,
        as_attachment=False,
        filename=f"carte_{prisonnier.numero_prisonnier}.pdf"
    )
from django.conf import settings
import os

def carte_prisonnier(request, pk):

    prisonnier = get_object_or_404(Prisonnier, pk=pk)

    buffer = BytesIO()

    largeur = 85.6 * mm
    hauteur = 54 * mm

    pdf = canvas.Canvas(buffer, pagesize=(largeur, hauteur))

    # ===== Fond bleu =====
    pdf.setFillColor(HexColor("#0B4EA2"))
    pdf.rect(0, 0, largeur, hauteur, fill=1)
    

    # ===== Chemins =====
    logo = os.path.join(
        settings.BASE_DIR,
        "prisonniers",
        "static",
        "prisonniers",
        "logo.png"
    )

    drapeau = os.path.join(
        settings.BASE_DIR,
        "prisonniers",
        "static",
        "prisonniers",
        "rdc.png"
    )

    # ===== Drapeau RDC =====
    if os.path.exists(drapeau):
        pdf.drawImage(
            drapeau,
            3 * mm,
            46 * mm,
            width=10 * mm,
            height=6 * mm,
            mask='auto'
        )

    # ===== Logo =====
    if os.path.exists(logo):
        pdf.drawImage(
            logo,
            67 * mm,
            41 * mm,
            width=15 * mm,
            height=10 * mm,
            mask='auto'
        )

    pdf.setFillColorRGB(1, 1, 1)

    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawCentredString(
        largeur / 2,
        49 * mm,
        "REPUBLIQUE DEMOCRATIQUE DU CONGO"
    )

    pdf.setFont("Helvetica-Bold", 8)

    pdf.drawCentredString(
        largeur / 2,
        45 * mm,
        "SYSTEME CARCERALNET"
    )
        # ==========================
    # PHOTO DU PRISONNIER
    # ==========================

    if prisonnier.photo:
        photo = prisonnier.photo.path

        if os.path.exists(photo):
            pdf.drawImage(
                photo,
                5 * mm,
                14 * mm,
                width=22 * mm,
                height=28 * mm,
                mask='auto'
            )

    # ==========================
    # INFORMATIONS
    # ==========================

    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 7)

    x = 30 * mm

    pdf.drawString(
        x,
        38 * mm,
        f"N° : {prisonnier.numero_prisonnier}"
    )

    pdf.drawString(
        x,
        34 * mm,
        f"Nom : {prisonnier.nom}"
    )

    pdf.drawString(
        x,
        30 * mm,
        f"Postnom : {prisonnier.postnom}"
    )

    pdf.drawString(
        x,
        26 * mm,
        f"Prénom : {prisonnier.prenom}"
    )

    pdf.drawString(
        x,
        22 * mm,
        f"Nationalité : {prisonnier.nationalite}"
    )

    pdf.drawString(
        x,
        18 * mm,
        f"Etat civil : {prisonnier.etat_civil}"
    )

    pdf.drawString(
        x,
        14 * mm,
        f"Cellule : {prisonnier.cellule}"
    )

    pdf.drawString(
        x,
        10 * mm,
        f"Entrée : {prisonnier.date_entree}"
    )

    pdf.drawString(
        x,
        6 * mm,
        f"Sortie : {prisonnier.date_sortie}"
    )

    # ==========================
    # QR CODE
    # ==========================

    qr = qrcode.make(
        f"CARCERALNET-{prisonnier.numero_prisonnier}"
    )

    qr_buffer = BytesIO()

    qr.save(qr_buffer, format="PNG")

    qr_buffer.seek(0)

    pdf.drawImage(
        ImageReader(qr_buffer),
        67 * mm,
        4 * mm,
        width=14 * mm,
        height=14 * mm
    )

    # ==========================
    # SIGNATURE
    # ==========================

    pdf.setFont("Helvetica", 5)

    pdf.drawString(
        52 * mm,
        2 * mm,
        "Direction Générale"
    )

    pdf.save()

    buffer.seek(0)

    return FileResponse(
        buffer,
        filename=f"{prisonnier.numero_prisonnier}.pdf",
        as_attachment=False
    )
def alertes(request):

    aujourdhui = Prisonnier.objects.filter(
        date_sortie=date.today()
    )

    retard = Prisonnier.objects.filter(
        date_sortie__lt=date.today(),
        statut="encours"
    )

    return render(
        request,
        "prisonniers/alertes.html",
        {
            "aujourdhui": aujourdhui,
            "retard": retard,
        }
    )
def alertes(request):

    aujourdhui = Prisonnier.objects.filter(
        date_sortie=date.today()
    )

    retard = Prisonnier.objects.filter(
        date_sortie__lt=date.today(),
        statut="encours"
    )

    return render(
        request,
        "prisonniers/alertes.html",
        {
            "aujourdhui": aujourdhui,
            "retard": retard,
        }
    )
def detail_prisonnier(request, pk):

    prisonnier = get_object_or_404(
        Prisonnier,
        pk=pk
    )

    return render(
        request,
        "prisonniers/detail_prisonnier.html",
        {
            "prisonnier": prisonnier
        }
    )
def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Nom d'utilisateur ou mot de passe incorrect."
            )

    return render(
        request,
        "prisonniers/login.html"
    )
def logout_view(request):

    logout(request)

    return redirect("login")
def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect("dashboard")

        messages.error(
            request,
            "Nom d'utilisateur ou mot de passe incorrect."
        )

    return render(
        request,
        "prisonniers/login.html"
    )
def logout_view(request):

    logout(request)

    return redirect("login")