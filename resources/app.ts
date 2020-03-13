import Dropzone from "dropzone";

$(() => {
  interface Image {
    filename: string;
    id: string;
  }
  interface DeleteData {
    success: boolean;
    deleted: string[];
  }

  let count: number = 0;
  $("#seagullDropzone").dropzone({
    url: "/upload",
    createImageThumbnails: false,
    acceptedFiles: "image/*",
    previewTemplate: `
    <div class="dz-preview dz-file-review p-4">
        <div class="dz-details">
          <div class="dz-filename"><span data-dz-name></span></div>
          <div class="dz-size" data-dz-size></div>
        </div>
        <div class="dz-error-mark"></div>
      </div>`,
    success(file: Dropzone.DropzoneFile, response?: Image) {
      $("span[data-dz-name]")[
        count
      ].innerHTML = `<a class='link' href='/${response?.filename}'>Link</a>`;
      count += 1;
      $(".image-links").append(
        `<li>
          <a class="link" href="/${response?.filename}">${response?.filename}</a>
          <input type="checkbox" name="image" image-id="${response?.id}" />
        </li>`,
      );
    },
    error(file: Dropzone.DropzoneFile, message?: Error | string) {
      count += 1;
      $(".dz-error-mark")[count].innerHTML = `Error: ${message}`;
    },
  });

  $("#settingsForm").submit((event) => {
    event.preventDefault();
    let images: string[] = [];
    $("input[name='image']:checked").each(function() {
      images.push(<string>$(this).attr("image-id"));
    });
    console.log(images);
    $.ajax({
      url: "/delete",
      method: "POST",
      contentType: "json",
      headers: {
        "Content-Type": "application/json",
      },
      data: JSON.stringify({ images }),
    }).done((data: DeleteData) => {
      data.deleted.forEach((item: string) => {
        $(`li[image-id="${item}"]`).remove();
      });
    });
  });

  $("#registerForm").submit((event) => {
    event.preventDefault();
    let username: string = <string>$("#registerUsername").val();
    let password: string = <string>$("#registerPassword").val();
    let email: string = <string>$("#registerEmail").val();
    $.ajax({
      url: "/register",
      method: "POST",
      contentType: "json",
      headers: {
        "Content-Type": "application/json",
      },
      data: JSON.stringify({ username, password, email }),
    }).done((data: Object) => {});
  });

  $("#loginForm").submit((event) => {
    event.preventDefault();
    let username: string = <string>$("#loginUsername").val();
    let password: string = <string>$("#loginPassword").val();
    $.ajax({
      url: "/login",
      method: "POST",
      contentType: "json",
      headers: {
        "Content-Type": "application/json",
      },
      data: JSON.stringify({ username, password }),
    }).done((data: Object) => {
      console.log(data);
    });
  });

  let checkedAll = false;
  $(".toggle-all").click(() => {
    if (!checkedAll) {
      $("input[type='checkbox']").prop("checked", true);
      checkedAll = true;
    } else {
      $("input[type='checkbox']").prop("checked", false);
      checkedAll = false;
    }
  });
});
