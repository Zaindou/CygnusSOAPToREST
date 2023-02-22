def serialize_respuesta_atr(respuesta_atr):
    """
    It converts the response object into a dictionary.
    
    :param respuesta_atr: This is the response object that is returned by the SOAP service
    :return: A dictionary with the following keys:
    """
    return {
        'n_num_cuo': respuesta_atr.n_num_cuo,
        'f_fecha': respuesta_atr.f_fecha,
        'n_sal_ini': respuesta_atr.n_sal_ini,
        'n_capital': respuesta_atr.n_capital,
        'n_int_1': respuesta_atr.n_int_1,
        'n_int_2': respuesta_atr.n_int_2,
        'n_int_3': respuesta_atr.n_int_3,
        'n_int_4': respuesta_atr.n_int_4,
        'n_int_5': respuesta_atr.n_int_5,
        'n_int_6': respuesta_atr.n_int_6,
        'n_int_7': respuesta_atr.n_int_7,
        'n_int_8': respuesta_atr.n_int_8,
        'n_int_9': respuesta_atr.n_int_9,
        'n_int_10': respuesta_atr.n_int_10,
        'n_cap_tf': respuesta_atr.n_cap_tf,
        'n_int_tf': respuesta_atr.n_int_tf,
        'n_total': respuesta_atr.n_total,
        'n_sal_fin': respuesta_atr.n_sal_fin,
        'n_intnom_1': respuesta_atr.n_intnom_1,
        'n_intnom_2': respuesta_atr.n_intnom_2,
        'n_intnom_3': respuesta_atr.n_intnom_3,
        'n_intnom_4': respuesta_atr.n_intnom_4,
        'n_intnom_5': respuesta_atr.n_intnom_5,
        'n_intnom_6': respuesta_atr.n_intnom_6,
        'n_intnom_7': respuesta_atr.n_intnom_7,
        'n_intnom_8': respuesta_atr.n_intnom_8,
        'n_intnom_9': respuesta_atr.n_intnom_9,
        'n_intnom_10': respuesta_atr.n_intnom_10,
        'n_salmor': respuesta_atr.n_salmor,
        's_estado': respuesta_atr.s_estado,
        'n_dias_mor': respuesta_atr.n_dias_mor
    }

def serialize_response(response):
    serialized_atr_list = []
    for atr in response.R_Liquidacion.LiquidacionAtr:
        serialized_atr_list.append(serialize_respuesta_atr(atr))
    
    return {
        'R_s_mensaje': response.R_s_mensaje,
        'R_Val_cuota': response.R_Val_cuota,
        'R_s_tasa': response.R_s_tasa,
        'R_ValorCuotaAsociado': response.R_ValorCuotaAsociado,
        'R_valtot_cre': response.R_valtot_cre,
        'R_pag_totcre': response.R_pag_totcre,
        'R_cuo_ini': response.R_cuo_ini,
        'R_cuo_ini_pen': response.R_cuo_ini_pen,
        'R_Liquidacion': {
            'LiquidacionAtr': serialized_atr_list
        }
    }
