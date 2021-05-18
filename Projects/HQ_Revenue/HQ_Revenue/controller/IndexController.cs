using System;
using System.Web.Http;
using System.Web.Http.Results;
namespace HQ_Revenue.controller
{
  public class IndexController
  {
    [HttpGet]
    public JsonResult GetHotelInfo()
    {

      return OkResult();
    }
  }
}
