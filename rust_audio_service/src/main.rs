use actix_web::{web, App, HttpRequest, HttpServer, HttpResponse, Result};

async fn stream_audio(req: HttpRequest) -> Result<HttpResponse> {
    // Placeholder: In production, check user access and stream file
    Ok(HttpResponse::Ok()
        .content_type("audio/mpeg")
        .body("AUDIO STREAM PLACEHOLDER"))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .route("/audio/{book_id}/{chapter}/", web::get().to(stream_audio))
    })
    .bind(("127.0.0.1", 8081))?
    .run()
    .await
}
