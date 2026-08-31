import { NextRequest, NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';
export const maxDuration = 300; // Allow long-running PyTorch deep model inferences on CPU

async function handleProxy(req: NextRequest, { params }: { params: { path: string[] } }) {
  const subpath = (params.path || []).join('/');
  const backendBase = (
    process.env.BACKEND_API_URL || 
    process.env.NEXT_PUBLIC_API_URL || 
    'http://127.0.0.1:8000'
  ).replace(/\/$/, '');
  
  const targetUrl = new URL(`${backendBase}/api/${subpath}`);
  
  // Forward all query search parameters
  req.nextUrl.searchParams.forEach((val, key) => {
    targetUrl.searchParams.append(key, val);
  });

  const headers = new Headers();
  req.headers.forEach((val, key) => {
    if (!['host', 'connection', 'content-length'].includes(key.toLowerCase())) {
      headers.set(key, val);
    }
  });

  try {
    const fetchOptions: RequestInit = {
      method: req.method,
      headers: headers,
      cache: 'no-store',
    };

    if (!['GET', 'HEAD'].includes(req.method)) {
      const bodyBlob = await req.blob();
      fetchOptions.body = bodyBlob;
    }

    const backendRes = await fetch(targetUrl.toString(), fetchOptions);
    const resHeaders = new Headers();
    backendRes.headers.forEach((val, key) => {
      if (!['transfer-encoding', 'content-encoding'].includes(key.toLowerCase())) {
        resHeaders.set(key, val);
      }
    });

    const responseBlob = await backendRes.blob();
    return new NextResponse(responseBlob, {
      status: backendRes.status,
      statusText: backendRes.statusText,
      headers: resHeaders,
    });
  } catch (err: any) {
    console.error(`[API Proxy Error] to ${targetUrl.toString()}:`, err);
    return NextResponse.json(
      { error: 'Backend connection error', detail: err.message },
      { status: 502 }
    );
  }
}

export const GET = handleProxy;
export const POST = handleProxy;
export const PUT = handleProxy;
export const DELETE = handleProxy;
export const PATCH = handleProxy;
