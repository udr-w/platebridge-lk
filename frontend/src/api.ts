export const API='/api';
export type User={id:number;email:string;name:string;role:string;donor_type?:string;organisation?:string;district:string;area:string;language:string;alias?:string;anonymous:boolean;active:boolean};
export type Listing={id:number;title:string;description:string;category:string;portions:number;available_portions:number;collection_deadline:string;allergens:string;ingredients:string;district:string;area:string;classification:'GREEN'|'AMBER'|'RED';safety_explanation:string;failed_checks:string;status:string;donor_name:string;distance_km?:number;timeline?:any[]};
export type Rescue={id:number;listing_id:number;listing_title:string;recipient_name:string;donor_name:string;portions:number;fulfilment:string;pickup_code:string;status:string;flagged:boolean;messages?:any[];timeline?:any[]};
export async function api<T>(path:string,options:RequestInit={}):Promise<T>{
 const token=localStorage.getItem('platebridge-token');
 const headers:Record<string,string>={'Content-Type':'application/json',...(options.headers as any||{})};if(token)headers.Authorization=`Bearer ${token}`;
 let res:Response;try{res=await fetch(`${API}${path}`,{...options,headers})}catch{throw new Error('The PlateBridge service is unavailable. Check that the backend is running.')}
 if(!res.ok){let msg=`Request failed (${res.status})`;try{const body=await res.json();msg=body.detail||msg}catch{msg=res.statusText||msg}throw new Error(msg)}
 return res.json();
}
