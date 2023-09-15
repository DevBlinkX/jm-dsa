    function deleteFile(e){
        $('[data-file-list]').empty();
        $('input[type="file"]').val('');
        $('[data-file-upload]').show()
        $('[data-upload]').hide();
    }

$(document).ready(function () {
    var fileNameIs;

    $(document).on('click','[data-reupload]', function () {
        $('[data-file-list],[data-step-1], [data-files-status] #importAcc').empty();
        $('[data-step-1]').show();
        $('[data-step-1]').append(`<form action="/api/dsa/leads/import/" method="post" data-bulk-form>
                                <input type="hidden" value="{{ csrf_token }}">
                                <div data-file-upload class="form-group">
                                    <input id="file-upload" type="file" name="file"  accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel,.csv"  />
                                    <label for="file-upload" id="file-drag" class="text-center">
                                        <i class="fa fa-upload"></i><br>
                                        CSV, XLS, XLSX<br>
                                        <span class="small">Maximum files size 50 MB</span>
                                        <br /><span id="file-upload-btn" class="button">Click to Upload</span>
                                    </label>
                                </div>
                                <div data-file-list>
                                </div>
                                <div class="d-lg-flex align-items-center">
                                    <a href="/static/doc/lead-template.csv" download="Lead Template Format.csv" class="btn gradient-btn rounded w-100 mx-2  py-2" type="button">
                                        <i class="fa fa-download"></i> Download Template
                                    </a>
                                    <button class="btn gradient-btn px-3 py-2 rounded w-100 mx-2" data-upload style="display:none;" type="submit">
                                        Upload
                                    </button>
                                </div>
                            </form>`)
        setTimeout(function () {   
                $('#file-upload').on('change',function(e){
                    fileNameIs = e.target.files[0].name;

                    $('[data-file-list]').append(`<div class="d-flex align-items-center justify-content-between border rounded px-3 py-3 mt-3 mb-5"><div class="d-flex align-items-center">
                                            <i class="fa fa-file-excel file-icon"></i>
                                            <div>
                                                <p class="m-0 text-dark h6 font-weight-500">${e.target.files[0].name}</p>
                                            </div>
                                        </div>
                                        <a href="#" onclick="deleteFile()"><i class="fa fa-trash text-gray-700"></i></a></div>`);
                    $('[data-upload]').show();
                    $('[data-file-upload]').hide();
                })
            }, 2000);
    })

    $(document).on('show.bs.modal','#bulkModal', function () {
    $('[data-step-1]').append(`<form action="/api/dsa/leads/import/" method="post" data-bulk-form>
                                <input type="hidden" value="{{ csrf_token }}">
                                <div data-file-upload class="form-group">
                                    <input id="file-upload" type="file" name="file"  accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel,.csv"  />
                                    <label for="file-upload" id="file-drag" class="text-center">
                                        <i class="fa fa-upload"></i><br>
                                        CSV, XLS, XLSX<br>
                                        <span class="small">Maximum files size 50 MB</span>
                                        <br /><span id="file-upload-btn" class="button">Click to Upload</span>
                                    </label>
                                </div>
                                <div data-file-list>
                                </div>
                                <div class="d-lg-flex align-items-center">
                                    <a href="/static/doc/lead-template.csv" download="Lead Template Format.csv" class="btn gradient-btn rounded w-100 mx-2 py-2" type="button">
                                        <i class="fa fa-download"></i> Download Template
                                    </a>
                                    <button class="btn gradient-btn px-3 rounded w-100 mx-2 py-2" data-upload style="display:none;" type="submit">
                                        Upload
                                    </button>
                                </div>
                            </form>`)
        
            setTimeout(function () {   
                $('#file-upload').on('change',function(e){
                    fileNameIs = e.target.files[0].name;

                    $('[data-file-list]').append(`<div class="d-flex align-items-center justify-content-between border rounded px-3 py-3 mt-3 mb-5"><div class="d-flex align-items-center">
                                            <i class="fa fa-file-excel file-icon"></i>
                                            <div>
                                                <p class="m-0 text-dark h6 font-weight-500">${e.target.files[0].name}</p>
                                            </div>
                                        </div>
                                        <a href="#" onclick="deleteFile()"><i class="fa fa-trash text-gray-700"></i></a></div>`);
                    $('[data-upload]').show();
                    $('[data-file-upload]').hide();
                })
            }, 2000);
    })


        $('body').on('submit', '[data-bulk-form]', function (e) {
            e.preventDefault();    
            var formData = new FormData(this);
            var href = $(this).attr("action");
            formData.append('dry_run','True');

            var formDataCreate = new FormData(this);
            var href = $(this).attr("action");
            formDataCreate.append('dry_run','False');

            $.ajax({
                url: href,
                type: 'POST',
                data: formData, 
                headers: {
                    "X-CSRFToken": '{{csrf_token}}',
                    Authorization: "Bearer " + localStorage.getItem("access-token"),
                },
                success: function (data) {
                    $('[data-step-1]').hide();
                    $('[data-files-status]').show();
                    
                    if(data.result.error == '0' || data.result.invalid == '0'){
                        $('[data-files-status] #importAcc').append(`<div class="mb-3">
                                <div class="" id="headingTwo">
                                <button class="btn w-100 p-0 text-left" type="button" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseTwo">
                                        <div class="d-flex align-items-center justify-content-between border border-success rounded px-3 py-3">
                                                        <div class="d-flex align-items-center">
                                                            <i class="fa fa-file-excel file-icon text-success"></i>
                                                            <div>
                                                                <p class="m-0 text-success h6 font-weight-500">${fileNameIs}</p>
                                                            </div>
                                                        </div>
                                                        <a href="#"><i class="fa fa-check-circle text-success"></i></a>
                                                    </div>         
                                    </button>
                                </div>
                                <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#importAcc">
                                <div class="acc-body">
                                    
                                </div>
                                </div>
                            </div><div class="d-lg-flex align-items-center">
                                <button class="btn info-btn rounded w-100 mx-2" data-dismiss="modal" aria-label="Close" type="button">
                                    Cancel
                                </button>
                                <button class="btn gradient-btn px-3 py-2 rounded w-100 mx-2" data-create type="button">
                                    Create
                                </button>
                            </div>`)
                        
                        $('body').on('click', '[data-create]', function (e) {
                            $.ajax({
                                url: href,
                                type: 'POST',
                                data: formDataCreate, 
                                headers: {
                                    "X-CSRFToken": '{{csrf_token}}',
                                    Authorization: "Bearer " + localStorage.getItem("access-token"),
                                },
                                success: function (data) {
                                    toastr.success('File import Successfully');
                                    $("#bulkModal").modal('hide');
                                    location.reload(true);
                                },
                                cache: false,
                                contentType: false,
                                processData: false
                            });
                        });
                    } else {
                        $('[data-files-status] #importAcc').append(` <div class="mb-3">
        <div class="" id="headingOne">
            <button class="btn w-100 p-0 text-left" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                <div class="d-flex align-items-center justify-content-between border border-danger rounded px-3 py-3">
                                <div class="d-flex align-items-center">
                                    <i class="fa fa-file-excel file-icon text-danger"></i>
                                    <div>
                                        <p class="m-0 text-danger h6 font-weight-500">${fileNameIs}</p>
                                    </div>
                                </div>
                                <a href="#"><i class="fa fa-angle-down text-danger"></i></a>
                            </div>            
            </button>
        </div>

        <div id="collapseOne" class="collapse" aria-labelledby="headingOne" data-parent="#importAcc">
        <div class="acc-body">
            
        </div>
        </div>
    </div> <div class="d-lg-flex align-items-center">
                                <button class="btn info-btn rounded w-100 mx-2" data-dismiss="modal" aria-label="Close" type="button">
                                    Cancel
                                </button>
                                <button class="btn gradient-btn px-3 py-2 rounded w-100 mx-2" data-reupload type="button">
                                    Re-Upload
                                </button>
                            </div>`)
                    }
                },
                 error: function (jqXHR, exception) {
                    if(jqXHR.status == 400){
                        $('[data-step-1]').hide();
                        $('[data-files-status]').show();
                        $('[data-files-status] #importAcc').append(` <div class="mb-3">
        <div class="" id="headingOne">
            <button class="btn w-100 p-0 text-left" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                <div class="d-flex align-items-center justify-content-between border border-danger rounded px-3 py-3">
                                <div class="d-flex align-items-center">
                                    <i class="fa fa-file-excel file-icon text-danger"></i>
                                    <div>
                                        <p class="m-0 text-danger h6 font-weight-500">${fileNameIs}</p>
                                    </div>
                                </div>
                                <a href="#"><i class="fa fa-angle-down text-danger"></i></a>
                            </div>            
            </button>
        </div>

        <div id="collapseOne" class="collapse" aria-labelledby="headingOne" data-parent="#importAcc">
        <div class="acc-body" data-acc-body>
            
        </div>
        </div>
    </div> <div class="d-lg-flex align-items-center">
                                <button class="btn info-btn rounded w-100 mx-2" data-dismiss="modal" aria-label="Close" type="button">
                                    Cancel
                                </button>
                                <button class="btn gradient-btn px-3 py-2 rounded w-100 mx-2" data-reupload type="button">
                                    Re-Upload
                                </button>
                            </div>`)
                    }
                    $.each(jqXHR.responseJSON.failed_rows, function (k, v) {
                        $('[data-acc-body').append(`<p class="small mb-1"><i class="fa fa-times-circle text-danger pr-2"></i>${v.error}</p>`);
                    });
                },
                cache: false,
                contentType: false,
                processData: false
            });

        });

    $(document).on('hide.bs.modal','#bulkModal', function () {
        $('[data-step-1').empty();
    })
})