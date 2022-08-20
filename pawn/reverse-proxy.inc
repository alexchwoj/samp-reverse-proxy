#if defined _REVERSEPROXY_INCLUDED
	#endinput
#endif
#define _REVERSEPROXY_INCLUDED

#include <a_samp>
#include <a_http>

#define REVERSEPROXY_SAFE
#define REVERSEPROXY_DEBUG
#define VALIDATOR_URL "loadbalancer.samp.valider.hyaxe.com:60422"

static playerAddress[MAX_PLAYERS][16];

stock GetPlayerRealIP(playerid, address[], len)
{
    format(address, len, playerAddress[playerid]);
    return 1;
}

public OnPlayerConnect(playerid)
{
    #if defined REVERSEPROXY_SAFE
    GetPlayerIp(playerid, playerAddress[playerid]);
    #else
    format(playerAddress[playerid], 16, "Loading...");
    #endif

	SetTimerEx("SendRequestToValidator", 5000, false, "i", playerid);

	#if defined RP_OnPlayerConnect
		return RP_OnPlayerConnect(playerid);
	#else
		return 1;
	#endif
}
#if defined _ALS_OnPlayerConnect
	#undef OnPlayerConnect
#else
	#define _ALS_OnPlayerConnect
#endif

#define OnPlayerConnect RP_OnPlayerConnect
#if defined RP_OnPlayerConnect
	forward RP_OnPlayerConnect(playerid);
#endif

forward SendRequestToValidator(playerid);
public SendRequestToValidator(playerid)
{
    if (IsPlayerConnected(playerid))
    {
        new ip_port[22];
        NetStats_GetIpPort(playerid, ip_port, sizeof(ip_port));

        new str_text[128];
        format(str_text, sizeof(str_text), ""VALIDATOR_URL"/address/real/%s", ip_port);

        #if defined REVERSEPROXY_DEBUG
        printf("[Reverse Proxy] URL = %s", str_text);
        #endif

        HTTP(playerid, HTTP_GET, str_text, "", "OnPlayerGetIPAddress");
    }
    return 1;
}

forward OnPlayerGetIPAddress(index, response_code, data[]);
public OnPlayerGetIPAddress(index, response_code, data[])
{
    if (response_code == 200)
	{
		if (data[0] == 'N')
		{
            #if defined REVERSEPROXY_SAFE
            GetPlayerIp(index, playerAddress[index]);
            #else
            format(playerAddress[index], 16, "Not Found");
            #endif
        }
        else
        {
            format(playerAddress[index], 16, data);
        }
    }
    return 1;
}