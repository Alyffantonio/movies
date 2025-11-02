from django.db import models


class Upload(models.Model):
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='uploads/', help_text="Arquivo XLSX ou CSV")
    processado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Upload"
        verbose_name_plural = "Uploads"
        ordering = ['-created_at']
        db_table = 'movie_upload'

    def __str__(self):
        return self.titulo


class Movie(models.Model):
    upload = models.ForeignKey(
        Upload,
        on_delete=models.CASCADE,
        related_name='filmes',
        help_text="Arquivo de origem deste conjunto de filmes."
    )

    titulo = models.CharField(max_length=255)
    ano = models.CharField(max_length=10, blank=True, null=True)
    elenco = models.TextField(blank=True, null=True)
    sinopse = models.TextField(blank=True, null=True)
    genero = models.CharField(max_length=255, blank=True, null=True)
    diretor = models.CharField(max_length=255, blank=True, null=True)
    nota_imdb = models.CharField(max_length=10, blank=True, null=True)

    nota_metacritic = models.CharField(max_length=10, blank=True, null=True)

    nota_rotten = models.CharField(max_length=10, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ['-created_at']
        db_table = 'movie'

    def __str__(self):
        return f"{self.titulo} ({self.ano})"


class Report(models.Model):
    upload = models.ForeignKey(
        Upload,
        on_delete=models.CASCADE,
        related_name='reports',
        help_text="Upload que originou este relatório."
    )

    arquivo = models.FileField(
        upload_to='reports/',
        help_text="Arquivo XLSX gerado após o processamento."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ['-created_at']

    def __str__(self):
        return f"Relatório de {self.upload.titulo}"
