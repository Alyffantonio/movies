document.addEventListener("DOMContentLoaded", function (event) {

    const form = document.getElementById('upload-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        toastr.info('Enviando, aguarde o processamento...', 'Upload Iniciado');

        const formData = new FormData();
        formData.append('titulo', document.getElementById('titulo').value);
        formData.append('arquivo', document.getElementById('arquivo').files[0]);

        fetch('/api/upload/', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errData => {
                        throw new Error(errData.error || 'Erro desconhecido no servidor.');
                    });
                }
                return response.json();
            })
            .then(data => {

                if (data.error) {
                    throw new Error(data.error);
                }

                toastr.success(`Processamento iniciado (ID: ${data.upload_id}). A página será recarregada.`, 'Sucesso!');

                form.reset();

                setTimeout(() => {
                    location.reload();
                }, 3000);
            })
            .catch(error => {
                console.error('Erro:', error);
                toastr.error(`Erro: ${error.message}`, 'Falha no Upload');
            });
    });

    window.api_delet = function(id) {
        fetch(`/api/delete/${id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Erro desconhecido');
                    });
                }
                return response.json();
            })
            .then(data => {
                toastr.success(`Relatorio excluido com Sucesso!`);

                setTimeout(() => location.reload(), 2000);
            })
            .catch(error => {
                console.error('Erro:', error);
                toastr.error(error.message || 'Erro ao processar requisição.', 'Erro!');
            });
    }
})